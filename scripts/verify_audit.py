"""Cross-check audit summaries with stdlib XLSX XML parsing; no openpyxl import."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ROW = "{" + NS["s"] + "}row"


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def records(path, decode_values=False, intro_diagnostics=None):
    with zipfile.ZipFile(path) as z:
        styles = ET.fromstring(z.read("xl/styles.xml"))
        format_ids = [int(x.get("numFmtId", "0")) for x in styles.find("s:cellXfs", NS)]
        wbpr = ET.fromstring(z.read("xl/workbook.xml")).find("s:workbookPr", NS)
        epoch_1904 = wbpr is not None and wbpr.get("date1904") in {"1", "true"}
        epoch = datetime(1904, 1, 1) if epoch_1904 else datetime(1899, 12, 30)
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            with z.open("xl/sharedStrings.xml") as f:
                for _, e in ET.iterparse(f, events=("end",)):
                    if e.tag == "{" + NS["s"] + "}si":
                        strings.append("".join(t.text or "" for t in e.findall(".//s:t", NS)))
                        e.clear()
        with z.open("xl/worksheets/sheet1.xml") as f:
            for _, row in ET.iterparse(f, events=("end",)):
                if row.tag != ROW:
                    continue
                data = {}
                for c in row.findall("s:c", NS):
                    key = re.sub(r"[0-9]", "", c.attrib["r"])
                    v = c.find("s:v", NS)
                    if c.get("t") == "s" and v is not None:
                        value = strings[int(v.text)]
                    elif c.get("t") == "inlineStr":
                        ts = c.findall(".//s:t", NS)
                        value = "".join(t.text or "" for t in ts) if ts else None
                    else:
                        value = v.text if v is not None else None
                    lexical_value = value
                    formula = c.find("s:f", NS)
                    fmt = format_ids[int(c.get("s", "0"))]
                    kind = "string" if c.get("t") in {"s", "inlineStr"} else "numeric_or_empty"
                    if formula is not None:
                        kind = "formula"
                        if decode_values:
                            value = "=" + (formula.text or "")
                    elif value is not None and c.get("t") not in {"s", "inlineStr", "e"} and fmt == 14:
                        # This supplied file uses builtin 14 for date cells; fail closed for unsupported date styles.
                        kind = "date_builtin_14"
                        if decode_values:
                            serial = float(value)
                            correction = 1 if not epoch_1904 and 0 < serial < 60 else 0
                            value = str(epoch + timedelta(days=serial + correction))
                    if intro_diagnostics is not None and key == "O" and lexical_value is not None and kind != "string":
                        intro_diagnostics.append({"excel_row": int(row.attrib["r"]), "cell": c.attrib["r"], "kind": kind,
                                                  "xml_type": c.get("t", "n"), "numFmtId": fmt,
                                                  "raw_lexical_chars": len(lexical_value), "decoded_chars": len(value or ""),
                                                  "raw_lexical_value": lexical_value if kind != "string" else "",
                                                  "decoded_value": value if kind != "string" else ""})
                    data[key] = value
                yield int(row.attrib["r"]), data
                row.clear()


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--run", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    args = a.parse_args()
    if args.out.exists():
        raise SystemExit("Verification output already exists; choose a new path")
    manifest = json.loads((args.run / "manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((args.run / "audit_summary.json").read_text(encoding="utf-8"))
    t, v = summary["teachers"], summary["vocabulary"]
    c, subsets, ids = collections.Counter(), collections.defaultdict(collections.Counter), set()
    whitespace_rows, empty_rows, malformed_rows, cap_rows, membrane_rows = [], [], [], [], []
    intro_diagnostics = []
    for rownum, cells in records(Path(manifest["inputs"]["teachers"]["path"]), decode_values=True, intro_diagnostics=intro_diagnostics):
        if rownum == 1:
            teacher_headers = {value: col for col, value in cells.items()}
            assert {"id", "deleted", "intro", "tags"}.issubset(teacher_headers), teacher_headers
            continue
        data = {name: cells.get(col) for name, col in teacher_headers.items()}
        if all(x is None or x == "" for x in data.values()):
            empty_rows.append(rownum)
            continue
        c["strict_nonempty"] += 1
        if all(x is None or not x.strip() for x in data.values()):
            whitespace_rows.append(rownum)
            continue
        c["trim_nonempty"] += 1
        if not re.fullmatch(r"[1-9][0-9]*", data.get("id") or ""):
            malformed_rows.append(rownum)
            continue
        ids.add(data["id"])
        c["valid"] += 1
        group = subsets[data.get("deleted") or ""]
        group["records"] += 1
        intro = data.get("intro") or ""
        group["intro_sum_chars"] += len(intro)
        if not intro.strip():
            group["intro_blank"] += 1
        tags = data.get("tags") or ""
        if not tags.strip():
            group["tags_blank"] += 1
        else:
            arr = json.loads(tags)
            assert isinstance(arr, list) and all(isinstance(x, str) for x in arr)
            group["assignments"] += len(arr)
        if len(intro) == 32767:
            cap_rows.append(rownum)
        if "膜分离" in intro:
            membrane_rows.append({"excel_row": rownum, "teacher_id": data["id"], "deleted": data.get("deleted")})
    l1, l2, children, nochildren, duplicates = set(), set(), [], [], collections.defaultdict(list)
    for rownum, cells in records(Path(manifest["inputs"]["vocabulary"]["path"])):
        if rownum == 1:
            vocabulary_headers = {value: col for col, value in cells.items()}
            assert {"family_tag", "primary_tag", "secondary_tag"}.issubset(vocabulary_headers), vocabulary_headers
            continue
        data = {name: cells.get(col) for name, col in vocabulary_headers.items()}
        if not any(x for x in data.values()):
            continue
        l1.add(data["family_tag"])
        l2.add(data["primary_tag"])
        arr = json.loads(data.get("secondary_tag") or "[]")
        assert isinstance(arr, list), (rownum, type(arr).__name__)
        children.extend(arr)
        for item in arr:
            duplicates[item].append(rownum)
        if not arr:
            nochildren.append(rownum)
    assertions = []
    def check(label, actual, expected):
        assertions.append({"check": label, "actual": actual, "expected": expected, "pass": actual == expected})
    check("trim-nonempty rows", c["trim_nonempty"], t["counts"]["nonempty_data_rows"])
    check("valid ID rows", c["valid"], t["counts"]["valid_id_rows"])
    check("unique IDs", len(ids), t["counts"]["unique_valid_ids"])
    check("malformed row numbers", malformed_rows, [x["excel_row"] for x in t["nonrecord_candidates"]])
    for deleted, actual in subsets.items():
        reported = t["by_deleted_raw"][deleted]
        for k, expected in [("records", reported["counts"]["records"]),
                            ("intro_sum_chars", reported["intro_characters"]["sum"]),
                            ("intro_blank", reported["missing_fields"].get("intro", 0)),
                            ("tags_blank", reported["missing_fields"].get("tags", 0)),
                            ("assignments", reported["counts"]["historical_assignment_occurrences"])]:
            check(f"deleted={deleted} {k}", actual[k], expected)
    check("vocabulary L1", len(l1), v["l1_unique_exact_strings"])
    check("vocabulary L2", len(l2), v["l2_unique_exact_strings"])
    check("vocabulary L3 occurrences", len(children), v["l3_occurrences"])
    check("vocabulary L3 unique strings", len(set(children)), v["l3_unique_exact_strings"])
    check("vocabulary rows without L3", nochildren, [r["excel_row"] for r in v["rows_without_l3"]])
    for key, info in manifest["inputs"].items():
        check(key + " unchanged SHA256", digest(Path(info["path"])), info["sha256_before"])
    for filename, expected in [("teacher_rows.csv", c["valid"]), ("historical_assignments.csv", sum(s["assignments"] for s in subsets.values()))]:
        with (args.run / filename).open(encoding="utf-8-sig", newline="") as f:
            check(filename + " rows", sum(1 for _ in csv.DictReader(f)), expected)
    output = {"checked_utc": datetime.now(timezone.utc).isoformat(), "method": "stdlib zipfile + ElementTree; does not import audit_inputs/openpyxl",
              "representation_rule": "data_only=False: formula text prefixed with =; builtin-14 serial dates decoded with workbook epoch to datetime string, matching main audit representation; raw lexical counts preserved separately",
              "intro_nonstring_or_formula_cells": intro_diagnostics,
              "intro_raw_vs_decoded_char_difference": sum(x["decoded_chars"] - x["raw_lexical_chars"] for x in intro_diagnostics),
              "teacher_columns_from_header": teacher_headers, "vocabulary_columns_from_header": vocabulary_headers,
              "verification_script_sha256": digest(Path(__file__)), "audit_directory": str(args.run.resolve()),
              "raw_xml_counts": dict(c), "whitespace_only_rows": whitespace_rows,
              "physically_empty_xml_rows": empty_rows, "by_deleted": {k: dict(x) for k, x in subsets.items()},
              "intro_at_32767_rows": cap_rows, "membrane_substring_mentions_not_gold": membrane_rows,
              "assertions": assertions, "all_pass": all(x["pass"] for x in assertions)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("all_pass", "raw_xml_counts", "whitespace_only_rows", "by_deleted")}, ensure_ascii=False, indent=2))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
