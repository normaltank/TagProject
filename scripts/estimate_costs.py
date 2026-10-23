"""Planning arithmetic over measured lengths; no tokenizer or model inference is run."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--verification", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        raise SystemExit("Choose a new output file")
    verification = json.loads(a.verification.read_text(encoding="utf-8"))
    assert verification["all_pass"]
    exclude = {x["excel_row"] for x in verification["intro_nonstring_or_formula_cells"]}
    with (a.run / "teacher_rows.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    scenarios = {}
    for key, subset in [("all_valid_id", rows), ("deleted_0", [r for r in rows if r["deleted_raw"] == "0"])]:
        texts = [r for r in subset if int(r["intro_chars"]) > 0 and int(r["excel_row"]) not in exclude]
        lengths = [int(r["intro_chars"]) for r in texts]
        chunks = [max(1, math.ceil((length - 150) / 1350)) for length in lengths]
        nchunks, nchars = sum(chunks), sum(lengths)
        overlap_chars = nchars + 150 * (nchunks - len(lengths))
        token_scenarios = []
        for chars_per_token in (1, 2, 4):
            input_tokens = overlap_chars / chars_per_token + nchunks * 1000
            output_tokens = nchunks * 300
            token_scenarios.append({"assumed_chars_per_token": chars_per_token,
                                    "assumed_input_tokens": input_tokens, "assumed_output_tokens": output_tokens,
                                    "illustrative_cost_currency_units_at_input_1_output_4_per_million": round((input_tokens + 4 * output_tokens) / 1e6, 2)})
        scenarios[key] = {"records_in_denominator": len(subset), "nonblank_string_cells_excluding_known_nontext_not_semantically_validated": len(texts),
                          "excluded_known_nontext_cells": sum(int(r["excel_row"]) in exclude for r in subset),
                          "measured_chars_after_known_nontext_exclusion": nchars, "illustrative_chunks": nchunks,
                          "measured_chars_with_assumed_chunk_overlap": overlap_chars,
                          "illustrative_rerank_pairs_top20_per_chunk": nchunks * 20,
                          "float32_768d_chunk_vectors_bytes": nchunks * 768 * 4,
                          "assumed_embed_wall_hours_at_20_to_200_chunks_per_second": [round(nchunks / (200 * 3600), 3), round(nchunks / (20 * 3600), 3)],
                          "assumed_rerank_wall_hours_at_50_to_500_pairs_per_second": [round(nchunks * 20 / (500 * 3600), 3), round(nchunks * 20 / (50 * 3600), 3)],
                          "token_sensitivity_not_actual_tokenization": token_scenarios}
    result = {"basis": "measured teacher_rows.csv; positive integer IDs; known numeric/date/formula intro cells excluded; remaining text quality not certified",
              "assumptions": {"chunk_chars": 1500, "overlap_chars": 150, "prompt_and_candidate_overhead_tokens_per_chunk": 1000,
                              "output_tokens_per_chunk": 300, "rerank_k": 20, "embedding_dimensions": 768,
                              "hypothetical_input_price_per_million": 1, "hypothetical_output_price_per_million": 4,
                              "price_currency": "unspecified common unit; NOT a provider quote", "tokenizer_run": False,
                              "model_run": False}, "scenarios": scenarios,
              "human_annotation_hypothesis": {"teachers": 600, "manuscripts": 400, "independent_reviewers": 2,
                                               "minutes_teacher": 15, "minutes_manuscript": 10, "arbitration_fraction": 0.25,
                                               "minutes_arbitration": 8,
                                               "initial_review_hours": 2 * (600 * 15 + 400 * 10) / 60,
                                               "arbitration_hours": 1000 * .25 * 8 / 60},
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
