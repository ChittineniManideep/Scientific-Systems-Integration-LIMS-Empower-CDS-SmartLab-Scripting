"""
Parses a simulated Empower-style chromatography results export, validates
each result against specification limits, and flags Out-of-Specification
(OOS) results — the OOS flag in a real GMP lab triggers a formal
investigation, so this classification is a meaningful, not cosmetic, step.
"""
import pandas as pd

chrom = pd.read_csv("data/empower_chromatography_export.csv")

chrom["in_spec"] = (chrom.result_pct_of_spec >= chrom.spec_low) & (chrom.result_pct_of_spec <= chrom.spec_high)
chrom["oos_flag"] = ~chrom.in_spec

chrom.to_csv("empower_cds/chromatography_validated.csv", index=False)

print(f"Total peak results: {len(chrom)}")
print(f"In-spec: {chrom.in_spec.sum()}, OOS: {chrom.oos_flag.sum()}")

oos_results = chrom[chrom.oos_flag]
if len(oos_results) > 0:
    print(f"\nOOS results requiring formal investigation per GMP deviation procedure:")
    print(oos_results[["sample_id", "peak_number", "result_pct_of_spec", "spec_low", "spec_high"]].to_string(index=False))

sample_level = chrom.groupby("sample_id").agg(
    peak_count=("peak_number", "count"),
    any_oos=("oos_flag", "any"),
).reset_index()
sample_level["sample_disposition"] = sample_level.any_oos.map({True: "FAIL — OOS investigation required", False: "PASS"})
sample_level.to_csv("empower_cds/sample_disposition.csv", index=False)

print(f"\nSample-level disposition: {sample_level.sample_disposition.eq('PASS').sum()} pass, "
      f"{sample_level.sample_disposition.str.contains('FAIL').sum()} fail")
