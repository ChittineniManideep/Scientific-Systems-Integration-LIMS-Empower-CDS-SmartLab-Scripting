"""
Synthetic LIMS sample records and Empower-style chromatography export data.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(16)

N_SAMPLES = 150
samples = pd.DataFrame({
    "sample_id": [f"SMPL-{50000+i}" for i in range(N_SAMPLES)],
    "product_batch": [f"BATCH-{2026}-{np.random.randint(100,999)}" for _ in range(N_SAMPLES)],
    "test_type": np.random.choice(["Assay (HPLC)", "Dissolution", "Impurities", "Content Uniformity", "pH"],
                                    N_SAMPLES, p=[0.30, 0.20, 0.25, 0.15, 0.10]),
    "received_date": [(datetime(2026, 7, 1) + timedelta(days=int(d))).strftime("%Y-%m-%d")
                       for d in np.random.uniform(0, 60, N_SAMPLES)],
})
samples.to_csv("data/lims_samples.csv", index=False)

chrom_samples = samples[samples.test_type.isin(["Assay (HPLC)", "Impurities"])]
chrom_rows = []
for _, s in chrom_samples.iterrows():
    n_peaks = np.random.randint(1, 4)
    for p in range(n_peaks):
        peak_area = np.random.normal(50000, 8000)
        retention_time = round(np.random.uniform(2.0, 12.0), 2)
        spec_low, spec_high = 95.0, 105.0
        result_pct = np.clip(np.random.normal(100, 3), 80, 120)
        chrom_rows.append({
            "sample_id": s.sample_id,
            "peak_number": p + 1,
            "retention_time_min": retention_time,
            "peak_area": round(peak_area, 1),
            "result_pct_of_spec": round(result_pct, 2),
            "spec_low": spec_low,
            "spec_high": spec_high,
        })

chrom_data = pd.DataFrame(chrom_rows)
chrom_data.to_csv("data/empower_chromatography_export.csv", index=False)

print(f"LIMS samples: {len(samples)}, chromatography peak records: {len(chrom_data)}")
