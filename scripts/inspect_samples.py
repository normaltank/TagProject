"""Local directed inspection excerpts; not a representative sample or a gold set."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
import openpyxl

PATS = {"kana": r"[\u3040-\u30ff]", "cyrillic": r"[\u0400-\u052f]", "hangul": r"[\uac00-\ud7af]",
        "arabic": r"[\u0600-\u06ff]", "thai": r"[\u0e00-\u0e7f]", "devanagari": r"[\u0900-\u097f]",
        "hebrew": r"[\u0590-\u05ff]", "greek": r"[\u0370-\u03ff]", "membrane": "膜分离"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        raise SystemExit("Choose a new inspection path")
    manifest = json.loads((a.run / "manifest.json").read_text(encoding="utf-8"))
    path = Path(manifest["inputs"]["teachers"]["path"])
    selected = {2, 3, 10, 80, 162, 548, 613, 1278, 1533, 1697, 1801, 1802, 2265, 2366, 2627, 2684,
                2926, 3253, 3798, 3854, 3905, 3959, 4088, 4248, 4992, 9855, 9984, 13850, 14280,
                17316, 18160, 23469, 23502, 25354, 25355, 34200, 65222, 88357, 91339}
    with (a.run / "teacher_rows.csv").open(encoding="utf-8-sig", newline="") as f:
        derived = list(csv.DictReader(f))
    for profile in ("Latin_without_Han", "other_or_nonletter"):
        selected.update(int(r["excel_row"]) for r in sorted((r for r in derived if r["script_profile"] == profile),
                                                            key=lambda r: -int(r["intro_chars"]))[:3])
    samples = []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=False)
    for rn, vals in enumerate(wb.worksheets[0].iter_rows(max_row=max(selected), values_only=True), 1):
        if rn not in selected:
            continue
        intro = str(vals[14] or "")
        spans = []
        for name, pat in PATS.items():
            hit = re.search(pat, intro)
            if hit:
                start, end = max(0, hit.start() - 60), min(len(intro), hit.start() + 180)
                spans.append({"trigger": name, "start_zero_based": start, "end_exclusive": end, "text": intro[start:end]})
        if not spans:
            spans = [{"trigger": "opening", "start_zero_based": 0, "end_exclusive": min(len(intro), 300), "text": intro[:300]}]
        try:
            domain = urlsplit(str(vals[13] or "")).hostname or ""
        except ValueError:
            domain = "unparsed"
        samples.append({"sheet": wb.worksheets[0].title, "excel_row": rn, "teacher_id_raw": vals[0],
                        "intro_cell": f"O{rn}", "intro_chars": len(intro),
                        "intro_sha256": hashlib.sha256(intro.encode("utf-8")).hexdigest(),
                        "opening": intro[:220], "spans": spans, "source_homepage_domain": domain,
                        "deleted_raw": vals[11], "tags_raw": vals[18],
                        "tail_fields_missing": [name for name, val in zip(["external_userid", "aminer_synced", "enrichment_status", "tags", "wecom_added", "is_interdisciplinary"], vals[15:21]) if val is None],
                        "populated_fields_in_nonrecord": [i + 1 for i, x in enumerate(vals) if x is not None] if not str(vals[0]).isdigit() else []})
    wb.close()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({"input_sha256": manifest["inputs"]["teachers"]["sha256_before"],
                               "selection": "directed by script profiles and anomalies; not population prevalence or gold labels", "samples": samples},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"samples": len(samples), "output": str(a.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
