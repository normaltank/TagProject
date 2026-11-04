"""Offline evidence-granularity profile, independent of any classifier.

The old validator supplies exact evidence/path checks, not semantic inference.
No request is built, model loaded, credential read, or network call performed.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from tagging.deepseek import (
    ClassificationError, InputRecord, Vocabulary, digest, exact_keys, file_hash,
    json_bytes, nonempty, redact, route, strict_json, validate_output,
)

CONTRACT_PATH = Path(__file__).resolve().parents[1] / "config/evidence_granularity_v1.json"
PROFILE_VERSION = "teacher_evidence_granularity_v1"


class ProfileVocabulary(Vocabulary):
    """Only this profile adds family source references; old Vocabulary is intact."""

    def __init__(self, rows, *, source_hash=None, sheet="fixture"):
        super().__init__(rows, source_hash=source_hash, sheet=sheet)
        self.family_refs = {}
        for row in sorted(rows, key=lambda item: item["source_row_id"]):
            family = row["family"]
            if family in self.family_refs:
                continue
            ref = f"row:{row['source_row_id']}:L1"
            self.family_refs[family] = ref
            self.registry[ref] = {
                "path": [family], "source_row_id": row["source_row_id"],
                "excel_row": row["excel_row"], "level": "L1",
                "cell": f"G{row['excel_row']}", "array_index": None,
            }
        self.hash = digest(json_bytes(self.registry))

    def ancestors(self, ref):
        entry = self.registry[ref]
        result = []
        if entry["level"] == "L3":
            result.append(f"row:{entry['source_row_id']}:L2")
        if entry["level"] != "L1":
            result.append(self.family_refs[entry["path"][0]])
        return result


def build_profile(data: dict, vocab: ProfileVocabulary) -> dict:
    """Validate a supplied judgement without changing its labels or meaning."""
    exact_keys(data, {"case_id", "source_version", "intro", "judgement"})
    nonempty(data["case_id"])
    nonempty(data["source_version"])
    nonempty(data["intro"])
    record = InputRecord(data["intro"], {"case_id": data["case_id"]})
    if route(record):
        raise ClassificationError("unsupported_intro")
    safe, masks = redact(record.value)
    checked = validate_output(data["judgement"], record,
                              {"redacted_intro": safe, "masks": masks}, vocab)
    directions = {d["id"]: d for d in checked["directions"]}
    for index, label in enumerate(checked["labels"]):
        if label["mapping_status"] == "supported" and any(
                directions[did]["support"] != "supported" for did in label["direction_ids"]):
            raise ClassificationError("mixed_direction_support", details={
                "field_path": f"labels[{index}].direction_ids"})

    supported = [label for label in checked["labels"] if label["mapping_status"] == "supported"]
    for child in supported:
        ancestors = vocab.ancestors(child["vocab_ref"])
        for parent in supported:
            if (parent["vocab_ref"] in ancestors
                    and set(parent["direction_ids"]) & set(child["direction_ids"])):
                # Reject instead of silently deleting/rewriting supplied judgements.
                raise ClassificationError("redundant_supported_ancestor")

    projections = []
    for label in checked["labels"]:
        label["user_level"] = len(label["path"]) - 1
        label["assertion_kind"] = "direct_evidence"
        label["assignment_status"] = "requires_review"
        label["temporal_status"] = "unknown"
        if label["mapping_status"] != "supported":
            continue
        for ref in vocab.ancestors(label["vocab_ref"]):
            entry = vocab.registry[ref]
            projections.append({
                "vocab_ref": ref, "path": entry["path"],
                "user_level": len(entry["path"]) - 1,
                "source_locator": dict(entry, sheet=vocab.sheet), "concept_id": None,
                "assertion_kind": "derived_projection", "derived_from": label["vocab_ref"],
                "direction_ids": label["direction_ids"],
                "counts_as_independent_expertise": False,
                "review_status": "requires_review",
            })
    for direction in checked["directions"]:
        direction["temporal_status"] = "unknown"
        direction["review_status"] = "requires_review"
    return dict(checked, profile_version=PROFILE_VERSION,
                case_id=data["case_id"], source_version=data["source_version"],
                intro_sha256=digest(data["intro"].encode("utf-8")),
                derived_projections=projections, review_status="requires_review",
                temporal_status="unknown", classifier_run=False)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True,
                        help="UTF-8 JSON: case_id, source_version, intro, judgement")
    parser.add_argument("--vocabulary", type=Path, required=True, help="Source vocabulary XLSX")
    parser.add_argument("--write-offline", action="store_true", help="Explicitly persist offline results")
    parser.add_argument("--out", type=Path, help="New output directory; never overwrites an existing directory")
    args = parser.parse_args(argv)
    try:
        if args.write_offline and args.out is None:
            raise ClassificationError("output_directory_required")
        if args.write_offline and args.out.exists():
            raise ClassificationError("output_directory_exists")
        raw = args.input.read_bytes()
        data = strict_json(raw)
        vocab = ProfileVocabulary.from_workbook(args.vocabulary)
        result = build_profile(data, vocab)
        contract = CONTRACT_PATH.read_bytes()
        manifest = {
            "profile_version": PROFILE_VERSION, "source_version": data["source_version"],
            "input_sha256": digest(raw), "contract_sha256": digest(contract),
            "module_sha256": file_hash(Path(__file__)),
            "base_validator_sha256": file_hash(Path(__file__).with_name("deepseek.py")),
            "vocabulary_source_sha256": vocab.source_hash,
            "vocabulary_catalogue_sha256": vocab.hash, "vocabulary_sheet": vocab.sheet,
            "result_sha256": digest(json_bytes(result)), "api_network_attempts": 0,
            "classifier_run": False, "semantic_validation": "not_performed",
        }
        if args.write_offline:
            # mkdir remains exclusive even if another process creates the target after our check.
            args.out.mkdir(parents=True, exist_ok=False)
            (args.out / "input.json").write_bytes(raw)
            (args.out / "result.json").write_bytes(json_bytes(result))
            (args.out / "contract.json").write_bytes(contract)
            (args.out / "catalogue.json").write_bytes(json_bytes(vocab.registry))
            (args.out / "manifest.json").write_bytes(json_bytes(manifest))
        print(json_bytes({"mode": "offline_written" if args.write_offline else "dry_run",
                          "case_id": data["case_id"], "direct_labels": len(result["labels"]),
                          "manifest": manifest}).decode("utf-8"))
        return 0
    except (ClassificationError, OSError) as exc:
        code = exc.code if isinstance(exc, ClassificationError) else "local_io_error"
        print(json_bytes({"error": code}).decode("utf-8"), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
