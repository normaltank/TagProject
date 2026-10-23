"""Synthetic validation and loopback HTTP only. Never uses a real API key."""
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import copy
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from tagging.deepseek import (
    ClassificationError, Config, DEFAULT_TEACHERS, DEFAULT_VOCABULARY, InputRecord,
    ROOT, Vocabulary, classify, completion_content, estimated_cost, file_hash,
    json_bytes, main, parse_rows, prepare, redact, request_completion,
    response_metadata, route, strict_json, teacher_records, validate_output,
)

FAKE_KEY = "mock-key-for-loopback-only"
TEXT = "研究方向：膜分离技术。"


def vocabulary():
    return Vocabulary([{"source_row_id": 101, "excel_row": 39, "family": "化学工程",
                        "primary": "化学工程与工业化学", "secondary": ["分离工程", "分离工程"]}])


def valid_output():
    return {"decision": "suggest", "reason": "明确研究方向", "directions": [
        {"id": "d1", "summary": "膜分离", "support": "supported", "evidence": [
            {"quote": TEXT, "occurrence": 1, "role": "explicit_direction"}]}],
        "labels": [{"vocab_ref": "row:101:L3:0", "path": ["化学工程", "化学工程与工业化学", "分离工程"],
                    "direction_ids": ["d1"], "mapping_status": "supported", "reason": "有研究方向证据"}],
        "gaps": []}


def envelope(data=None, **changes):
    value = {"model": "mock-model", "choices": [{"finish_reason": "stop", "message": {
        "content": json.dumps(valid_output() if data is None else data, ensure_ascii=False)}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120}}
    value.update(changes)
    return value


@contextmanager
def mock_server(replies):
    requests = []
    pending = list(replies)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            requests.append({"path": self.path, "authorization": self.headers.get("Authorization"),
                             "body": self.rfile.read(int(self.headers["Content-Length"]))})
            reply = pending.pop(0) if pending else {"status": 500, "body": b"exhausted"}
            if reply.get("delay"):
                time.sleep(reply["delay"])
            body = reply.get("body", json_bytes(envelope()))
            try:
                self.send_response(reply.get("status", 200))
                for name, value in reply.get("headers", {}).items():
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/chat/completions", requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.vocab = vocabulary()
        self.record = InputRecord(TEXT, {"kind": "synthetic"})
        self.prepared = prepare(self.record, self.vocab, Config())

    def validate(self, data):
        return validate_output(data, self.record, self.prepared, self.vocab)

    def test_valid_offsets_paths_and_no_formal_assignment(self):
        output = self.validate(valid_output())
        quote = output["directions"][0]["evidence"][0]
        self.assertEqual(TEXT[quote["start"]:quote["end"]], quote["quote"])
        self.assertEqual(output["labels"][0]["source_locator"]["excel_row"], 39)
        self.assertIsNone(output["labels"][0]["concept_id"])
        self.assertFalse(output["formal_assignment_written"])
        self.assertEqual(output["semantic_validation"], "not_performed")

    def test_repeated_quote_uses_explicit_occurrence(self):
        record = InputRecord(TEXT + "\n" + TEXT, {})
        data = valid_output()
        data["directions"][0]["evidence"][0]["occurrence"] = 2
        result = validate_output(data, record, prepare(record, self.vocab, Config()), self.vocab)
        self.assertEqual(result["directions"][0]["evidence"][0]["start"], len(TEXT) + 1)

    def test_duplicate_names_keep_distinct_source_occurrences(self):
        self.assertEqual(len(self.vocab.registry), 3)
        data = valid_output()
        data["labels"][0]["vocab_ref"] = "row:101:L3:1"
        self.assertEqual(self.validate(data)["labels"][0]["source_locator"]["array_index"], 1)

    def test_l2_is_allowed(self):
        data = valid_output()
        data["labels"][0].update(vocab_ref="row:101:L2", path=["化学工程", "化学工程与工业化学"])
        self.assertEqual(self.validate(data)["labels"][0]["source_locator"]["level"], "L2")

    def test_abstain_and_gap_review_are_allowed(self):
        self.validate({"decision": "abstain", "reason": "无足够信息", "directions": [], "labels": [], "gaps": []})
        data = valid_output()
        data.update(decision="needs_review", labels=[], gaps=[{"description": "膜分离细节", "direction_ids": ["d1"],
                    "reason": "保留原描述", "proposed_action": "keep_description"}])
        self.assertEqual(len(self.validate(data)["gaps"]), 1)

    def test_unknown_reference_and_wrong_path_rejected(self):
        for field, value in (("vocab_ref", "row:999:L2"), ("path", ["编造"]), ("vocab_ref", "row:101:L3:999")):
            with self.subTest(field=field, value=value):
                data = valid_output()
                data["labels"][0][field] = value
                with self.assertRaises(ClassificationError): self.validate(data)

    def test_fabricated_quote_and_occurrence_rejected(self):
        for field, value in (("quote", "不存在的证据"), ("occurrence", 2), ("occurrence", True), ("occurrence", 0)):
            with self.subTest(field=field, value=value):
                data = valid_output()
                data["directions"][0]["evidence"][0][field] = value
                with self.assertRaises(ClassificationError): self.validate(data)

    def test_masked_evidence_rejected(self):
        record = InputRecord("姓名：张三\n" + TEXT, {}, name_to_redact="张三")
        prepared = prepare(record, self.vocab, Config())
        data = valid_output()
        data["directions"][0]["evidence"][0]["quote"] = "██"
        with self.assertRaisesRegex(ClassificationError, "evidence_overlaps_redaction"):
            validate_output(data, record, prepared, self.vocab)

    def test_sole_teaching_project_or_paper_cannot_support_label(self):
        for role in ("teaching", "navigation", "employment", "administrative", "project", "publication"):
            with self.subTest(role=role):
                data = valid_output()
                data["directions"][0]["evidence"][0]["role"] = role
                with self.assertRaisesRegex(ClassificationError, "insufficient_declared_support"): self.validate(data)

    def test_weak_direction_cannot_support_positive_label(self):
        data = valid_output()
        data["directions"][0]["support"] = "weak"
        with self.assertRaises(ClassificationError): self.validate(data)
        data["labels"][0]["mapping_status"] = "scope_review"
        self.assertEqual(self.validate(data)["labels"][0]["mapping_status"], "scope_review")

    def test_structural_errors_are_quarantined(self):
        cases = []
        d = valid_output(); d["unexpected"] = "field"; cases.append(d)
        d = valid_output(); d["labels"] *= 2; cases.append(d)
        d = valid_output(); d["labels"][0]["direction_ids"] = ["missing"]; cases.append(d)
        d = valid_output(); d["directions"] *= 2; cases.append(d)
        d = valid_output(); d["decision"] = "abstain"; cases.append(d)
        d = valid_output(); d["labels"] = []; cases.append(d)
        d = valid_output(); d["decision"] = []; cases.append(d)
        d = valid_output(); d["directions"][0]["support"] = {}; cases.append(d)
        d = valid_output(); d["directions"][0]["evidence"][0]["role"] = []; cases.append(d)
        for index, data in enumerate(cases):
            with self.subTest(index=index):
                result, _ = classify(self.record, self.vocab, Config(), mode="replay", replay=envelope(data))
                self.assertEqual(result["status"], "quarantined")
                self.assertNotIn("output", result)

    def test_personal_and_secret_response_rejected(self):
        for text in ("foo@example.test", "sk-12345678901234567890"):
            d = valid_output(); d["reason"] = text
            with self.assertRaises(ClassificationError): self.validate(d)

    def test_no_arbitrary_label_count_cap(self):
        rows = [{"source_row_id": i + 1, "excel_row": i + 2, "family": "F", "primary": f"P{i}", "secondary": []} for i in range(40)]
        vocab = Vocabulary(rows)
        data = valid_output()
        data["labels"] = [{"vocab_ref": f"row:{i+1}:L2", "path": ["F", f"P{i}"], "direction_ids": ["d1"],
                           "mapping_status": "scope_review", "reason": "合成结构边界测试"} for i in range(40)]
        result = validate_output(data, self.record, prepare(self.record, vocab, Config()), vocab)
        self.assertEqual(len(result["labels"]), 40)


class InputAndEnvelopeTests(unittest.TestCase):
    def test_local_routes_skip_client(self):
        values = [(None, "empty_intro"), (" \n", "empty_intro"), (2005, "numeric_intro"),
                  ("2005", "numeric_text_intro"), (datetime(2026, 6, 8), "date_intro"),
                  ("2026-06-08", "date_text_intro"), ("=-某大学", "formula_intro"),
                  ("#NAME?", "excel_error_intro"), ("�" * 10, "garbled_intro")]
        def forbidden(*_): raise AssertionError("client must not be called")
        for value, expected in values:
            with self.subTest(expected=expected):
                result, preview = classify(InputRecord(value, {}), vocabulary(), Config(), mode="live", client=forbidden)
                self.assertEqual(result["routing"], expected)
                self.assertEqual(result["status"], "routed_without_api")
                self.assertIsNone(preview)

    def test_redaction_preserves_offsets_and_payload_excludes_columns(self):
        text = "姓名：张三\n邮箱abc@example.test 电话13812345678\n" + TEXT
        record = InputRecord(text, {"teacher_id": 12345, "old_tag": "OLD_SHOULD_NEVER_SEND"}, name_to_redact="张三")
        prepared = prepare(record, vocabulary(), Config(), "sk-secret123456789012")
        payload = prepared["payload"]
        user = strict_json(payload["messages"][1]["content"])
        self.assertEqual(set(user), {"intro", "vocabulary"})
        self.assertEqual(len(user["intro"]), len(text))
        self.assertEqual(user["intro"].index(TEXT), text.index(TEXT))
        for forbidden in ("张三", "abc@example.test", "13812345678", "OLD_SHOULD_NEVER_SEND", "12345", "sk-secret"):
            self.assertNotIn(forbidden, json.dumps(payload, ensure_ascii=False))

    def test_intro_and_request_budget_reject_without_truncation(self):
        record = InputRecord(TEXT, {})
        for config, code in ((Config(max_intro_chars=2), "intro_budget_exceeded"),
                             (Config(max_request_bytes=2), "request_budget_exceeded")):
            result, preview = classify(record, vocabulary(), config, mode="live")
            self.assertEqual(result["error"], code)
            self.assertIsNone(preview)
            self.assertEqual(record.value, TEXT)

    def test_json_fences_nan_duplicate_and_bad_json_rejected(self):
        for raw in ("```json\n{}\n```", '{"x":NaN}', '{"x":1,"x":2}', "{", ""):
            with self.subTest(raw=raw):
                with self.assertRaises(ClassificationError): strict_json(raw)

    def test_length_empty_and_bad_envelope_rejected(self):
        cases = [None, {}, {"choices": []}, {"choices": [{"finish_reason": "stop", "message": {"content": ""}}]},
                 {"choices": [{"finish_reason": "length", "message": {"content": "{}"}}]},
                 {"choices": [{"finish_reason": "content_filter", "message": {"content": "{}"}}]}]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ClassificationError): completion_content(case)

    def test_unknown_usage_is_null_and_cost_requires_rates(self):
        self.assertIsNone(response_metadata({})["usage"])
        self.assertIsNone(estimated_cost(None, None))
        self.assertIsNone(estimated_cost({"prompt_tokens": 10}, None))
        rates = {"currency": "test-unit", "input_cache_hit_per_million": 1, "input_cache_miss_per_million": 2, "output_per_million": 3}
        cost = estimated_cost({"prompt_tokens": 10, "completion_tokens": 5}, rates)
        self.assertAlmostEqual(cost["amount"], 35 / 1e6)
        self.assertIn("user_supplied", cost["basis"])

    def test_config_rejects_secret_bad_endpoint_and_unbounded_retries(self):
        for config in ({"api_key": "NEVER_STORE"}, {"max_retries": 4}, {"timeout_seconds": float("nan")},
                       {"endpoint": "http://example.test/chat"}, {"endpoint": "https://user:secret@example.test/chat"},
                       {"endpoint": "https://example.test/chat?key=secret"}):
            with self.subTest(keys=list(config)):
                with self.assertRaises(ClassificationError): Config.from_mapping(config)

    def test_explicit_rows_parser_has_no_range_or_batch_live(self):
        self.assertEqual(parse_rows("10,4"), [10, 4])
        for raw in ("1", "2-100000", "2,2", "0", ",10"):
            with self.subTest(raw=raw):
                with self.assertRaises(Exception): parse_rows(raw)


class HttpTests(unittest.TestCase):
    def config(self, endpoint, **kwargs):
        return Config(endpoint=endpoint, timeout_seconds=1, **kwargs)

    def test_real_loopback_http_contract(self):
        with mock_server([{}]) as (url, requests):
            result, _ = classify(InputRecord(TEXT, {}), vocabulary(), self.config(url), mode="live", key=FAKE_KEY)
        self.assertEqual(result["status"], "validated_pending_review")
        self.assertEqual(requests[0]["authorization"], "Bearer " + FAKE_KEY)
        payload = strict_json(requests[0]["body"])
        self.assertEqual(payload["thinking"], {"type": "disabled"})
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertNotIn(FAKE_KEY, requests[0]["body"].decode())
        self.assertEqual(result["usage"]["total_tokens"], 120)

    def test_429_retry_then_success(self):
        with mock_server([{"status": 429}, {}]) as (url, requests):
            _, attempts = request_completion({}, self.config(url), FAKE_KEY, sleeper=lambda _: None)
        self.assertEqual(len(requests), 2)
        self.assertEqual([a["http_status"] for a in attempts], [429, 200])

    def test_500_exhausts_bounded_retry(self):
        with mock_server([{"status": 500}, {"status": 500}]) as (url, requests):
            with self.assertRaises(ClassificationError) as cm:
                request_completion({}, self.config(url), FAKE_KEY, sleeper=lambda _: None)
        self.assertEqual(len(requests), 2)
        self.assertEqual(len(cm.exception.details["attempts"]), 2)

    def test_401_not_retried_or_error_body_logged(self):
        with mock_server([{"status": 401, "body": FAKE_KEY.encode()}]) as (url, requests):
            result, _ = classify(InputRecord(TEXT, {}), vocabulary(), self.config(url), mode="live", key=FAKE_KEY)
        self.assertEqual(len(requests), 1)
        self.assertEqual(result["status"], "quarantined")
        self.assertNotIn(FAKE_KEY, json.dumps(result))

    def test_timeout_is_unsuccessful(self):
        with mock_server([{"delay": 0.1}]) as (url, requests):
            with self.assertRaises(ClassificationError) as cm:
                request_completion({}, Config(endpoint=url, timeout_seconds=0.02, max_retries=0), FAKE_KEY)
        self.assertEqual(cm.exception.code, "network_or_timeout_error")
        self.assertEqual(len(requests), 1)

    def test_redirect_not_followed(self):
        with mock_server([{"status": 307, "headers": {"Location": "http://127.0.0.1:1/leak"}}]) as (url, requests):
            with self.assertRaises(ClassificationError):
                request_completion({}, self.config(url), FAKE_KEY, sleeper=lambda _: None)
        self.assertEqual(len(requests), 1)

    def test_oversized_response_and_invalid_json(self):
        for reply, limit, error in (({"body": b"x" * 200}, 100, "response_budget_exceeded"),
                                    ({"body": b"{"}, 100, "invalid_json")):
            with self.subTest(error=error):
                with mock_server([reply]) as (url, _):
                    with self.assertRaises(ClassificationError) as cm:
                        request_completion({}, self.config(url, max_response_bytes=limit), FAKE_KEY)
                self.assertEqual(cm.exception.code, error)
                self.assertEqual(len(cm.exception.details["attempts"]), 1)

    def test_no_key_no_network(self):
        result, _ = classify(InputRecord(TEXT, {}), vocabulary(), Config(), mode="live", key=None)
        self.assertEqual(result["error"], "missing_api_key")
        self.assertEqual(result["attempts"], [])


class LocalIntegrationTests(unittest.TestCase):
    def test_real_vocabulary_counts_and_teacher_typed_routes(self):
        vocab = Vocabulary.from_workbook(DEFAULT_VOCABULARY)
        self.assertEqual((len(vocab.rows), len(vocab.registry)), (139, 1535))
        records = teacher_records(DEFAULT_TEACHERS, [10, 4, 5205, 8099, 8730])
        self.assertEqual([route(r) for r in records], [None, "empty_intro", "numeric_intro", "date_intro", "formula_intro"])
        prepared = prepare(records[0], vocab, Config())
        self.assertEqual(prepared["intro_chars"], 93)
        self.assertLess(prepared["request_bytes"], Config().max_request_bytes)
        user = strict_json(prepared["payload"]["messages"][1]["content"])
        self.assertEqual(set(user), {"intro", "vocabulary"})
        self.assertNotIn("teacher_id", user)

    def test_cli_dry_run_is_default_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"DEEPSEEK_API_KEY": FAKE_KEY}):
            out = Path(temp) / "run"
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(main(["--text", TEXT, "--out", str(out)]), 0)
                self.assertEqual(main(["--text", TEXT, "--out", str(out)]), 2)
            result = strict_json((out / "results.json").read_text(encoding="utf-8"))[0]
            manifest = strict_json((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "dry_run_no_classification")
            self.assertEqual(manifest["api_network_attempts"], 0)
            self.assertNotIn(FAKE_KEY, "".join(p.read_text(encoding="utf-8") for p in out.iterdir()))

    def test_cli_rejects_multiple_live_before_reading_data(self):
        with tempfile.TemporaryDirectory() as temp, redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--teacher-rows", "10,4", "--live", "--out", str(Path(temp) / "run")]), 2)


if __name__ == "__main__":
    unittest.main()
