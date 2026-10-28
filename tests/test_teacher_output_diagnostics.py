"""Synthetic CLI regressions; replay only, with socket access denied.

These fixtures represent failure types, never the unavailable pilot responses.
Set TAGPROJECT_DIAGNOSTIC_EVIDENCE to an empty directory to retain CLI artifacts.
"""
from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import openpyxl

from tagging.deepseek import main


TEXT = "研究方向：合成主题。"


def synthetic_output():
    return {
        "decision": "suggest", "reason": "纯合成诊断材料",
        "directions": [{"id": "d1", "summary": "合成主题", "support": "supported",
                        "evidence": [{"quote": TEXT, "occurrence": 1,
                                      "role": "explicit_direction"}]}],
        "labels": [{"vocab_ref": "row:1:L2", "path": ["合成学科", "合成主题"],
                    "direction_ids": ["d1"], "mapping_status": "supported",
                    "reason": "合成标签映射"}],
        "gaps": [],
    }


class CliOutputDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        destination = os.environ.get("TAGPROJECT_DIAGNOSTIC_EVIDENCE")
        if destination:
            self.root = Path(destination) / self._testMethodName
            self.root.mkdir(parents=True, exist_ok=False)
        else:
            temp = tempfile.TemporaryDirectory()
            self.addCleanup(temp.cleanup)
            self.root = Path(temp.name)

    def replay(self, data, text=TEXT, extra_args=(), mode="replay"):
        # Load a real synthetic XLSX through the public CLI vocabulary argument.
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["id", "deleted", "family_tag", "primary_tag", "secondary_tag"])
        sheet.append([1, 0, "合成学科", "合成主题", "[]"])
        vocabulary = self.root / "synthetic_vocabulary.xlsx"
        workbook.save(vocabulary)
        workbook.close()
        intro = self.root / "synthetic_intro.txt"
        intro.write_text(text, encoding="utf-8")
        response = self.root / "synthetic_response.json"
        response.write_text(json.dumps({
            "model": "synthetic-replay-not-historical", "choices": [{
                "finish_reason": "stop", "message": {
                    "content": json.dumps(data, ensure_ascii=False)}}],
        }, ensure_ascii=False), encoding="utf-8")
        out = self.root / "cli_output"
        stdout, stderr = io.StringIO(), io.StringIO()
        attempts = []

        def deny_connect(*args, **kwargs):
            attempts.append("blocked_socket_connect")
            raise AssertionError("Offline regression attempted network access")

        # A clean environment means the CLI never reads an existing credential.
        with patch.dict(os.environ, {}, clear=True), patch.object(socket.socket, "connect", deny_connect), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            mode_args = ["--response-file", str(response)] if mode == "replay" else []
            code = main(["--text-file", str(intro), "--vocabulary", str(vocabulary),
                         *mode_args, "--out", str(out), *extra_args])
        (self.root / "cli_stdout.txt").write_text(stdout.getvalue(), encoding="utf-8")
        (self.root / "cli_stderr.txt").write_text(stderr.getvalue(), encoding="utf-8")
        (self.root / "network_guard.json").write_text(json.dumps({
            "socket_connect_attempts": attempts, "environment_cleared": True,
            "mode": mode, "real_classification_api_requests": 0}), encoding="utf-8")
        self.assertEqual(attempts, [])
        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["api_network_attempts"], 0)
        self.assertFalse(manifest["api_key_present"])
        result = json.loads((out / "results.json").read_text(encoding="utf-8"))[0]
        review = (out / "REVIEW.md").read_text(encoding="utf-8")
        return code, result, review

    def test_duplicate_label_reports_safe_field_location(self):
        data = synthetic_output()
        data["labels"].append(copy.deepcopy(data["labels"][0]))
        code, result, review = self.replay(data)
        self.assertEqual((code, result["status"], result["error"]),
                         (2, "quarantined", "duplicate_label"))
        self.assertNotIn("output", result)
        # The Issue requires both the violation type and its field location.
        self.assertEqual(result["error_details"].get("field_path"), "labels[1].vocab_ref")
        self.assertIn("labels[1].vocab_ref", review)

    def test_wrong_path_reports_safe_field_location(self):
        data = synthetic_output()
        data["labels"][0]["path"] = []
        code, result, review = self.replay(data)
        self.assertEqual((code, result["status"], result["error"]),
                         (2, "quarantined", "vocabulary_path_mismatch"))
        self.assertNotIn("output", result)
        self.assertEqual(result["error_details"].get("field_path"), "labels[0].path")
        self.assertIn("labels[0].path", review)

    def test_insufficient_support_reports_safe_field_location(self):
        data = synthetic_output()
        data["directions"][0]["support"] = "weak"
        code, result, review = self.replay(data)
        self.assertEqual((code, result["status"], result["error"]),
                         (2, "quarantined", "insufficient_declared_support"))
        self.assertNotIn("output", result)
        self.assertEqual(result["error_details"].get("field_path"), "labels[0].mapping_status")
        self.assertIn("labels[0].mapping_status", review)

    def test_sole_teaching_evidence_cannot_claim_supported_direction(self):
        text = "教授课程：合成主题。"
        data = synthetic_output()
        data.update(decision="needs_review", labels=[])
        data["directions"][0]["evidence"][0].update(quote=text, role="teaching")
        code, result, _ = self.replay(data, text=text)
        # This checks contradictory declared metadata, not meaning inferred from text.
        self.assertEqual((code, result["status"]), (2, "quarantined"))
        self.assertNotIn("output", result)

    def test_teaching_scope_review_cannot_claim_supported_direction(self):
        text = "教授课程：合成主题。"
        data = synthetic_output()
        data["decision"] = "needs_review"
        data["labels"][0]["mapping_status"] = "scope_review"
        data["directions"][0]["evidence"][0].update(quote=text, role="teaching")
        code, result, _ = self.replay(data, text=text)
        self.assertEqual((code, result["status"]), (2, "quarantined"))
        self.assertEqual(result["error_details"]["field_path"], "directions[0].support")

    def test_interest_remains_weak_scope_review(self):
        text = "兴趣：合成主题。"
        data = synthetic_output()
        data["decision"] = "needs_review"
        data["directions"][0]["support"] = "weak"
        data["directions"][0]["evidence"][0].update(quote=text, role="research_interest")
        data["labels"][0]["mapping_status"] = "scope_review"
        code, result, _ = self.replay(data, text=text)
        self.assertEqual((code, result["status"]), (0, "validated_pending_review"))
        self.assertEqual(result["output_contract_version"], "teacher_output_v2")
        self.assertEqual(result["output"]["semantic_validation"], "not_performed")

    def test_explicit_legacy_replay_keeps_original_validation_policy(self):
        text = "教授课程：合成主题。"
        data = synthetic_output()
        data.update(decision="needs_review", labels=[])
        data["directions"][0]["evidence"][0].update(quote=text, role="teaching")
        code, result, review = self.replay(data, text=text,
                                         extra_args=("--response-contract", "teacher_output_v1"))
        self.assertEqual((code, result["status"]), (0, "validated_pending_review"))
        self.assertEqual(result["output_contract_version"], "teacher_output_v1")
        self.assertIn("teacher_output_v1", review)

    def test_valid_result_has_locally_computed_unicode_offsets(self):
        data = synthetic_output()
        code, result, _ = self.replay(data, text="🧪" + TEXT)
        self.assertEqual((code, result["status"]), (0, "validated_pending_review"))
        evidence = result["output"]["directions"][0]["evidence"][0]
        self.assertEqual((evidence["start"], evidence["end"]), (1, 11))
        self.assertEqual(result["output"]["semantic_validation"], "not_performed")
        self.assertFalse(result["formal_assignment_written"])

    def test_insufficient_material_is_abstain_not_failure(self):
        code, result, _ = self.replay({"decision": "abstain", "reason": "资料不足",
                                     "directions": [], "labels": [], "gaps": []}, "简介待补充。")
        self.assertEqual((code, result["status"], result["output"]["decision"]),
                         (0, "validated_pending_review", "abstain"))
        self.assertEqual(result["output"]["labels"], [])

    def test_fabricated_quote_is_quarantined_at_quote_field(self):
        data = synthetic_output()
        data["directions"][0]["evidence"][0]["quote"] = "合成但不存在的引文"
        code, result, review = self.replay(data)
        self.assertEqual((code, result["error"]), (2, "evidence_not_in_intro"))
        self.assertEqual(result["error_details"], {"field_path": "directions[0].evidence[0].quote"})
        self.assertNotIn("合成但不存在的引文", json.dumps(result, ensure_ascii=False) + review)
        self.assertNotIn("output", result)

    def test_out_of_range_occurrence_cannot_create_offsets(self):
        data = synthetic_output()
        data["directions"][0]["evidence"][0]["occurrence"] = 99
        code, result, _ = self.replay(data)
        self.assertEqual((code, result["error"]), (2, "evidence_not_in_intro"))
        self.assertNotIn("output", result)

    def test_model_supplied_out_of_bounds_offsets_are_not_trusted(self):
        data = synthetic_output()
        data["directions"][0]["evidence"][0].update(start=-1, end=9999)
        code, result, _ = self.replay(data)
        self.assertEqual((code, result["error"]), (2, "invalid_structure"))
        self.assertEqual(result["error_details"], {"field_path": "directions[0].evidence[0]"})
        self.assertNotIn("output", result)

    def test_unknown_vocabulary_identity_diagnostic_never_echoes_model_value(self):
        data = synthetic_output()
        data["labels"][0]["vocab_ref"] = "UNTRUSTED_MODEL_VALUE_993"
        code, result, review = self.replay(data)
        self.assertEqual((code, result["error"]), (2, "unknown_vocabulary_reference"))
        self.assertEqual(result["error_details"], {"field_path": "labels[0].vocab_ref"})
        self.assertNotIn("UNTRUSTED_MODEL_VALUE_993", json.dumps(result) + review)

    def test_honest_weak_teaching_can_remain_scope_review(self):
        text = "教授课程：合成主题。"
        data = synthetic_output()
        data["decision"] = "needs_review"
        data["directions"][0]["support"] = "weak"
        data["directions"][0]["evidence"][0].update(quote=text, role="teaching")
        data["labels"][0]["mapping_status"] = "scope_review"
        code, result, _ = self.replay(data, text=text)
        self.assertEqual((code, result["output"]["labels"][0]["mapping_status"]), (0, "scope_review"))
        self.assertEqual(result["output"]["semantic_validation"], "not_performed")

    def test_uncertain_range_can_remain_scope_review(self):
        data = synthetic_output()
        data["decision"] = "needs_review"
        data["labels"][0].update(mapping_status="scope_review", reason="仅部分表达，包含关系尚未确认")
        code, result, review = self.replay(data)
        self.assertEqual((code, result["output"]["labels"][0]["mapping_status"]), (0, "scope_review"))
        self.assertIn("scope_review", review)

    def test_honest_weak_direction_without_labels_is_reviewable(self):
        text = "单篇题名：合成主题。"
        data = synthetic_output()
        data.update(decision="needs_review", labels=[])
        data["directions"][0]["support"] = "weak"
        data["directions"][0]["evidence"][0].update(quote=text, role="publication")
        code, result, _ = self.replay(data, text=text)
        self.assertEqual((code, result["output"]["directions"][0]["support"]), (0, "weak"))

    def test_default_remains_dry_run(self):
        code, result, _ = self.replay(synthetic_output(), mode="dry_run")
        self.assertEqual((code, result["status"]), (0, "dry_run_no_classification"))
        self.assertNotIn("output", result)

    def test_legacy_contract_option_cannot_enable_live_or_dry_compatibility(self):
        for live_args in ([], ["--live"]):
            with self.subTest(live=bool(live_args)), patch.dict(os.environ, {}, clear=True), \
                    patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")), \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as stderr:
                code = main(["--text", TEXT, "--response-contract", "teacher_output_v1", *live_args])
            self.assertEqual(code, 2)
            self.assertIn("response_contract_requires_replay", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
