"""Checks and experiment sizing, computed only from results/*.csv.

1. Does merchant density go with usage? (district-level rank correlation, with a bootstrap CI)
2. How many districts would a district-level (geo) experiment need? Uses the real year-over-year
   variation of transactions per user across districts.
Writes results/sizing.md. Associations here are not causal.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

N = NormalDist()


def spearman(x: pd.Series, y: pd.Series) -> float:
    return float(x.rank().corr(y.rank()))


def bootstrap_ci(x: pd.Series, y: pd.Series, n: int = 2000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n):
        idx = rng.integers(0, len(x), len(x))
        vals.append(
            spearman(x.iloc[idx].reset_index(drop=True), y.iloc[idx].reset_index(drop=True))
        )
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(lo), float(hi)


def districts_per_arm(sd: float, effect: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Two-arm comparison of mean district outcomes (normal approximation)."""
    z = N.inv_cdf(1 - alpha / 2) + N.inv_cdf(power)
    return math.ceil(2 * (z * sd / effect) ** 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, default=Path("results"))
    args = ap.parse_args()
    r = args.results

    d = pd.read_csv(r / "06_district_latest.csv")
    d = d[d["users"] >= 100000].reset_index(drop=True)
    rho = spearman(d["merchants_per_1000_users"], d["txns_per_user"])
    lo, hi = bootstrap_ci(d["merchants_per_1000_users"], d["txns_per_user"])
    rho_ticket = spearman(d["avg_ticket_inr"], d["txns_per_user"])

    g = pd.read_csv(r / "11_district_growth.csv")
    cutoff = g["txns_per_user"].quantile(0.25)
    target = g[g["txns_per_user"] < cutoff]
    sd_all = float(g["txns_per_user_growth_yoy_pct"].std())
    sd_target = float(target["txns_per_user_growth_yoy_pct"].std())
    mean_target = float(target["txns_per_user_growth_yoy_pct"].mean())
    mean_all = float(g["txns_per_user_growth_yoy_pct"].mean())

    z = N.inv_cdf(0.975) + N.inv_cdf(0.8)
    mde = z * sd_target * math.sqrt(2 / (len(target) // 2))
    rows = []
    for effect in (3, 5, 8):
        n = districts_per_arm(sd_target, effect)
        rows.append(f"| +{effect} points | {n} | {2 * n} |")

    md = f"""# Checks and experiment sizing

All inputs come from the SQL results in this folder. These are associations in aggregate data, not proof of cause.

## 1. Do more merchants go with more usage?

Across {len(d)} districts with 100k+ registered users (latest quarter):

- Merchants per 1,000 registered users vs transactions per user: Spearman rank correlation **{rho:.2f}** (95% bootstrap CI {lo:.2f} to {hi:.2f}).
- Average ticket size vs transactions per user: Spearman **{rho_ticket:.2f}**.

{"Merchant density has only a weak link to usage across districts, so adding merchants alone is unlikely to be the main fix for low engagement." if abs(rho) < 0.3 else "Merchant density has a clear link to usage across districts."}

## 2. Sizing a district-level experiment

Outcome: year-over-year growth in transactions per user. Across {len(g)} districts it has mean {mean_all:.1f}% and standard deviation {sd_all:.1f} points. In the {len(target)} lowest-engagement districts (below {cutoff:.1f} transactions per user) the mean is {mean_target:.1f}% and the standard deviation {sd_target:.1f} points.

Districts needed per arm to detect an extra improvement in that growth rate (80% power, 5% significance, two-sided, using the low-engagement districts' variation):

| Detectable extra growth | Districts per arm | Total districts |
|---|---:|---:|
{chr(10).join(rows)}

The {len(target)} low-engagement districts are the available pool. Split in two ({len(target) // 2} per arm), the smallest extra growth the test could reliably detect is about **{mde:.1f} points**. This uses district-level variation only; a real test would also match districts on their pre-period trend, which would shrink the variance and the detectable effect.
"""
    (r / "sizing.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
