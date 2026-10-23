"""Read selected teacher intros without historical tags; export redacted reading cues only."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import openpyxl

ROWS = [2, 4, 10, 80, 613, 1278, 1533, 1697, 2627, 2926, 3253, 3854, 4992, 5205, 8099, 8730]
CUES = re.compile(r"研究方向|研究领域|主要从事|研究兴趣|科研方向|科研领域|主要研究|研究重点|研究内容|research interests|research areas|research focuses|focuses on|膜分离", re.I)
SECTION_END = re.compile(r"近期学术成果|期刊论文|会议论文|代表性论文|论文发表|主要学术|社会兼职|研究概况|荣誉|科研项目|发表论文|联系电话|电子邮箱|Email|开设课程|任教课程|研究生招生学科|教育背景|工作经历|【教育经历】|Contact us|Experience:|Teaching:|Awards|Person Types:", re.I)
PII = re.compile(r"[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}|(?<!\d)(?:\+?86[- ]?)?(?:1[3-9]\d{9}|0\d{2,3}[- ]?\d{7,8})(?!\d)")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--teachers", type=Path, required=True)
    ap.add_argument("--audit-manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        raise SystemExit("Choose a new reading-pack path")
    audit = json.loads(a.audit_manifest.read_text(encoding="utf-8"))
    before = sha(a.teachers)
    assert before == audit["inputs"]["teachers"]["sha256_before"]
    wb = openpyxl.load_workbook(a.teachers, read_only=True, data_only=False)
    ws = wb["teacher_20261022"]
    cases = []
    # Never iterate S/tags: only A:O is consumed. Prior context exposure is declared separately.
    for rn, cells in enumerate(ws.iter_rows(max_row=max(ROWS), max_col=15), 1):
        if rn not in ROWS:
            continue
        raw_id, person_name, deleted, intro_cell = cells[0].value, str(cells[1].value or ""), cells[11].value, cells[14]
        raw = intro_cell.value
        text = raw if isinstance(raw, str) else ""
        name_pattern = re.compile(r"\s*".join(re.escape(c) for c in person_name.strip())) if person_name.strip() else None
        def redact(s):
            t = PII.sub("[联系方式已隐藏]", s)
            return name_pattern.sub("[姓名已隐藏]", t) if name_pattern else t
        intervals = []
        if rn == 2627:
            intervals.append((0, min(len(text), 105), "article_page_header"))
        elif rn == 1533:
            menu = text.find("English")
            menu_end = text.find("首页", menu)
            if menu >= 0 and menu_end > menu:
                intervals.append((menu, menu_end, "language_menu_only"))
        elif rn == 3854:
            intervals.append((0, min(len(text), 30), "unreadable_opening"))
        elif intro_cell.data_type == "f":
            intervals.append((0, len(text), "formula_not_prose"))
        for hit in CUES.finditer(text):
            start, end = hit.start(), min(len(text), hit.start() + 380)
            boundary = SECTION_END.search(text, hit.end(), end)
            if boundary:
                end = boundary.start()
            if not any(start >= left and start < right for left, right, _ in intervals):
                intervals.append((start, end, hit.group()))
        intervals = intervals[:14]
        cases.append({"teacher_id": str(raw_id), "sheet": ws.title, "excel_row": rn, "field": "intro", "cell": f"O{rn}",
                      "deleted_raw": deleted, "python_value_type": type(raw).__name__, "excel_cell_type": intro_cell.data_type,
                      "intro_chars_if_text": len(text), "intro_sha256_if_text": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None,
                      "scalar_display_if_not_text": str(raw) if raw is not None and not isinstance(raw, str) else None,
                      "reading_cues": [{"start_zero_based": start, "end_exclusive": end, "trigger": trigger,
                                        "display_text": redact(text[start:end]), "display_redacted": redact(text[start:end]) != text[start:end]}
                                       for start, end, trigger in intervals if end > start]})
    wb.close()
    assert sha(a.teachers) == before
    result = {"prepared_utc": datetime.now(timezone.utc).isoformat(), "source_sha256": before,
              "script_sha256": sha(Path(__file__)), "selected_excel_rows": ROWS,
              "historical_tags_in_workpack": False, "prior_audit_context_exposure": True,
              "not_independent_or_fully_blinded": True, "no_model_inference": True,
              "offset_convention": "Unicode code points; zero-based start, exclusive end; display may be redacted; final evidence must be verified against original cell",
              "cases": cases}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"cases": len(cases), "historical_tags_in_workpack": False, "input_unchanged": True, "out": str(a.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
