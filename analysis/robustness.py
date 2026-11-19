"""How sensitive is the headline "6% of volume" engagement-gap estimate to my own choices?

The headline uses: districts with 100k+ registered users, the bottom quarter by transactions per
user, lifted to the median. This script varies each of those choices and reports the result.
Reads results/06_district_latest.csv; writes results/robustness.csv and results/robustness.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def gap_share(d: pd.DataFrame, min_users: int, bottom_q: float, target_q: float) -> dict:
    pool = d[d["users"] >= min_users]
    tpu = pool["txns_per_user"]
    cutoff, target = tpu.quantile(bottom_q), tpu.quantile(target_q)
    low = pool[tpu < cutoff]
    extra = ((target - low["txns_per_user"]) * low["users"]).sum()
    return {
        "min_registered_users": min_users,
        "bottom_share_of_districts": bottom_q,
        "lifted_to_percentile": target_q,
        "districts_considered": len(pool),
        "districts_in_gap": len(low),
        "extra_txns_m_per_quarter": round(extra / 1e6, 1),
        "extra_pct_of_all_txns": round(100 * extra / d["txns"].sum(), 1),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, default=Path("results"))
    args = ap.parse_args()
    d = pd.read_csv(args.results / "06_district_latest.csv")

    rows = []
    for min_users in (50_000, 100_000, 200_000):
        for bottom_q in (0.20, 0.25, 0.33):
            for target_q in (0.40, 0.50, 0.60):
                rows.append(gap_share(d, min_users, bottom_q, target_q))
    out = pd.DataFrame(rows)
    out.to_csv(args.results / "robustness.csv", index=False)

    base = out[
        (out.min_registered_users == 100_000)
        & (out.bottom_share_of_districts == 0.25)
        & (out.lifted_to_percentile == 0.50)
    ].iloc[0]
    md = f"""# Robustness of the engagement-gap estimate

Headline: districts with 100k+ registered users, the bottom quarter by transactions per user, lifted to the median: **{base.extra_pct_of_all_txns:.1f}%** of all transactions per quarter ({base.extra_txns_m_per_quarter:,.0f} million).

(This recomputes the figure from district ratios rounded to one decimal, so it differs from the exact SQL result in `08_engagement_gap_total.csv` by about 0.1%.)

Varying all three choices ({len(out)} combinations), the estimate ranges from **{out.extra_pct_of_all_txns.min():.1f}% to {out.extra_pct_of_all_txns.max():.1f}%** of volume (median of the combinations {out.extra_pct_of_all_txns.median():.1f}%).

| Registered-user floor | Bottom share lifted | Lifted to | Districts in gap | Extra transactions (m per quarter) | % of all transactions |
|---:|---:|---:|---:|---:|---:|
"""
    for r in out.itertuples():
        md += f"| {r.min_registered_users:,} | {r.bottom_share_of_districts:.0%} | {r.lifted_to_percentile:.0%} percentile | {r.districts_in_gap} | {r.extra_txns_m_per_quarter:,.1f} | {r.extra_pct_of_all_txns:.1f}% |\n"
    md += "\nThe direction never changes: under every combination tested, lifting low-usage districts adds volume. The size depends on how ambitious the target is (lifting to the 40th percentile adds far less than to the 60th), so the headline should be read as an order of magnitude, not a forecast.\n"
    (args.results / "robustness.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
