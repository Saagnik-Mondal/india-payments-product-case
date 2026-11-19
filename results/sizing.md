# Checks and experiment sizing

All inputs come from the SQL results in this folder. These are associations in aggregate data, not proof of cause.

## 1. Do more merchants go with more usage?

Across 680 districts with 100k+ registered users (latest quarter):

- Merchants per 1,000 registered users vs transactions per user: Spearman rank correlation **0.10** (95% bootstrap CI 0.02 to 0.17).
- Average ticket size vs transactions per user: Spearman **0.05**.

Merchant density has only a weak link to usage across districts, so adding merchants alone is unlikely to be the main fix for low engagement.

## 2. Sizing a district-level experiment

Outcome: year-over-year growth in transactions per user. Across 672 districts it has mean 11.4% and standard deviation 5.7 points. In the 168 lowest-engagement districts (below 31.0 transactions per user) the mean is 10.3% and the standard deviation 6.2 points.

Districts needed per arm to detect an extra improvement in that growth rate (80% power, 5% significance, two-sided, using the low-engagement districts' variation):

| Detectable extra growth | Districts per arm | Total districts |
|---|---:|---:|
| +3 points | 67 | 134 |
| +5 points | 24 | 48 |
| +8 points | 10 | 20 |

The 168 low-engagement districts are the available pool. Split in two (84 per arm), the smallest extra growth the test could reliably detect is about **2.7 points**. This uses district-level variation only; a real test would also match districts on their pre-period trend, which would shrink the variance and the detectable effect.
