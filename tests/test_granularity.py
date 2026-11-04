"""Synthetic profile checks; no teacher workbook or model is used."""
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import openpyxl

from tagging.deepseek import ClassificationError, Vocabulary
from tagging.granularity import ProfileVocabulary, build_profile, main


ROWS = [
    {"source_row_id": 8, "excel_row": 3, "family": "甲", "primary": "中类", "secondary": ["同名", "中类"]},
    {"source_row_id": 3, "excel_row": 2, "family": "甲", "primary": "无细类", "secondary": []},
    {"source_row_id": 9, "excel_row": 4, "family": "乙", "primary": "中类", "secondary": ["同名"]},
]
TEXT = "研究方向：合成领域。另有教学兴趣。"


def input_case(ref="row:8:L3:0", path=None):
    vocab = ProfileVocabulary(ROWS)
    return {"case_id": "synthetic", "source_version": "synthetic-v1", "intro": TEXT,
            "judgement": {"decision": "suggest", "reason": "合成显式判断",
                          "directions": [{"id": "d1", "summary": "合成领域", "support": "supported",
                                          "evidence": [{"quote": "研究方向：合成领域。", "occurrence": 1,
                                                        "role": "explicit_direction"}]}],
                          "labels": [{"vocab_ref": ref, "path": path or vocab.registry[ref]["path"],
                                      "direction_ids": ["d1"], "mapping_status": "supported", "reason": "合成映射"}],
                          "gaps": []}}


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.vocab = ProfileVocabulary(ROWS)

    def test_levels_projection_and_source_identity_without_changing_judgement(self):
        for ref, level, ancestors in [("row:8:L3:0", 2, ["row:8:L2", "row:3:L1"]),
                                       ("row:3:L2", 1, ["row:3:L1"]), ("row:3:L1", 0, [])]:
            with self.subTest(ref=ref):
                data = input_case(ref)
                original = deepcopy(data)
                result = build_profile(data, self.vocab)
                self.assertEqual(data, original)
                self.assertEqual([x["user_level"] for x in result["labels"]], [level])
                self.assertEqual([x["vocab_ref"] for x in result["derived_projections"]], ancestors)
                self.assertTrue(all(not x["counts_as_independent_expertise"] for x in result["derived_projections"]))
                self.assertEqual(result["review_status"], "requires_review")
                self.assertEqual(result["semantic_validation"], "not_performed")
                self.assertFalse(result["formal_assignment_written"])
                e = result["directions"][0]["evidence"][0]
                self.assertEqual(TEXT[e["start"]:e["end"]], e["quote"])
        self.assertEqual(self.vocab.registry["row:3:L1"]["cell"], "G2")
        self.assertNotIn("row:3:L1", Vocabulary(ROWS).registry)
        # Same name at another parent or level is never substituted.
        for ref in ("row:9:L3:0", "row:8:L3:1", "row:8:L2"):
            self.assertEqual(build_profile(input_case(ref), self.vocab)["labels"][0]["vocab_ref"], ref)

    def test_scope_review_keeps_status_and_never_projects_or_downpushes(self):
        data = input_case("row:3:L1")
        data["judgement"]["labels"][0]["mapping_status"] = "scope_review"
        result = build_profile(data, self.vocab)
        self.assertEqual(result["labels"][0]["mapping_status"], "scope_review")
        self.assertEqual(len(result["labels"]), 1)
        self.assertEqual(result["derived_projections"], [])

    def test_weak_declared_roles_cannot_be_supported_at_any_level(self):
        for ref in ("row:8:L3:0", "row:3:L2", "row:3:L1"):
            for role in ("teaching", "research_interest", "employment", "navigation"):
                data = input_case(ref)
                direction = data["judgement"]["directions"][0]
                direction["evidence"][0]["role"] = role
                with self.assertRaises(ClassificationError):
                    build_profile(data, self.vocab)
                direction["support"] = "weak"
                data["judgement"]["labels"][0]["mapping_status"] = "scope_review"
                self.assertEqual(build_profile(data, self.vocab)["derived_projections"], [])

    def test_mixed_directions_and_redundant_ancestors_are_rejected(self):
        data = input_case()
        weak = deepcopy(data["judgement"]["directions"][0])
        weak.update(id="d2", support="weak")
        data["judgement"]["directions"].append(weak)
        data["judgement"]["labels"][0]["direction_ids"].append("d2")
        with self.assertRaisesRegex(ClassificationError, "mixed_direction_support"):
            build_profile(data, self.vocab)
        data = input_case()
        data["judgement"]["labels"].append(input_case("row:8:L2")["judgement"]["labels"][0])
        with self.assertRaisesRegex(ClassificationError, "redundant_supported_ancestor"):
            build_profile(data, self.vocab)
        # The broader assertion can belong to a separate direction.
        d2 = deepcopy(data["judgement"]["directions"][0])
        d2["id"] = "d2"
        data["judgement"]["directions"].append(d2)
        data["judgement"]["labels"][1]["direction_ids"] = ["d2"]
        self.assertEqual(len(build_profile(data, self.vocab)["labels"]), 2)

    def test_invalid_path_ref_and_quote_are_rejected_not_repaired(self):
        for key, bad in [("path", ["乙", "中类", "同名"]), ("vocab_ref", "row:0:L1")]:
            data = input_case()
            data["judgement"]["labels"][0][key] = bad
            with self.assertRaises(ClassificationError):
                build_profile(data, self.vocab)
        data = input_case()
        data["judgement"]["directions"][0]["evidence"][0]["quote"] = "不存在的引文"
        with self.assertRaisesRegex(ClassificationError, "evidence_not_in_intro"):
            build_profile(data, self.vocab)


class CliTests(unittest.TestCase):
    def test_preview_has_no_writes_credentials_model_or_network_and_write_is_exclusive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["id", "deleted", "unused1", "unused2", "primary_tag", "secondary_tag", "family_tag"])
            for row in sorted(ROWS, key=lambda r: r["excel_row"]):
                sheet.append([row["source_row_id"], 0, None, None, row["primary"],
                              json.dumps(row["secondary"], ensure_ascii=False), row["family"]])
            vocab_path = root / "vocabulary.xlsx"
            workbook.save(vocab_path)
            workbook.close()
            source = root / "input.json"
            source.write_text(json.dumps(input_case(), ensure_ascii=False), encoding="utf-8")
            out = root / "result"
            args = ["--input", str(source), "--vocabulary", str(vocab_path), "--out", str(out)]
            before = sorted(p.name for p in root.iterdir())
            def deny(*args, **kwargs):
                raise AssertionError("Forbidden network/model/credential access")
            original_getitem = os._Environ.__getitem__
            def guard_environment(env, key):
                # argparse/gettext may read locale variables; credentials remain forbidden.
                if any(word in str(key).upper() for word in ("KEY", "TOKEN", "SECRET", "PASSWORD")):
                    deny()
                return original_getitem(env, key)
            with patch.object(socket.socket, "connect", deny), patch("os.getenv", deny), \
                    patch.object(os._Environ, "__getitem__", guard_environment), \
                    patch("tagging.deepseek.prepare", deny), patch("tagging.deepseek.request_completion", deny), \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(main(args), 0)
                self.assertFalse(out.exists())
                self.assertEqual(sorted(p.name for p in root.iterdir()), before)
                self.assertEqual(main(args + ["--write-offline"]), 0)
                saved = {p.name: p.read_bytes() for p in out.iterdir()}
                self.assertEqual(main(args + ["--write-offline"]), 2)
                self.assertEqual(saved, {p.name: p.read_bytes() for p in out.iterdir()})
                empty = root / "empty"
                empty.mkdir()
                self.assertEqual(main([*args[:-1], str(empty), "--write-offline"]), 2)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["api_network_attempts"], 0)
            self.assertEqual((out / "input.json").read_bytes(), source.read_bytes())


if __name__ == "__main__":
    unittest.main()
