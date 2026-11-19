# Robustness of the engagement-gap estimate

Headline: districts with 100k+ registered users, the bottom quarter by transactions per user, lifted to the median: **6.0%** of all transactions per quarter (2,334 million).

(This recomputes the figure from district ratios rounded to one decimal, so it differs from the exact SQL result in `08_engagement_gap_total.csv` by about 0.1%.)

Varying all three choices (27 combinations), the estimate ranges from **3.8% to 9.6%** of volume (median of the combinations 5.8%).

| Registered-user floor | Bottom share lifted | Lifted to | Districts in gap | Extra transactions (m per quarter) | % of all transactions |
|---:|---:|---:|---:|---:|---:|
| 50,000 | 20% | 40% percentile | 141 | 1,450.5 | 3.8% |
| 50,000 | 20% | 50% percentile | 141 | 1,864.0 | 4.8% |
| 50,000 | 20% | 60% percentile | 141 | 2,187.0 | 5.7% |
| 50,000 | 25% | 40% percentile | 176 | 1,659.0 | 4.3% |
| 50,000 | 25% | 50% percentile | 176 | 2,189.5 | 5.7% |
| 50,000 | 25% | 60% percentile | 176 | 2,603.9 | 6.7% |
| 50,000 | 33% | 40% percentile | 232 | 1,888.4 | 4.9% |
| 50,000 | 33% | 50% percentile | 232 | 2,630.4 | 6.8% |
| 50,000 | 33% | 60% percentile | 232 | 3,210.2 | 8.3% |
| 100,000 | 20% | 40% percentile | 136 | 1,515.1 | 3.9% |
| 100,000 | 20% | 50% percentile | 136 | 1,912.4 | 4.9% |
| 100,000 | 20% | 60% percentile | 136 | 2,251.1 | 5.8% |
| 100,000 | 25% | 40% percentile | 170 | 1,792.2 | 4.6% |
| 100,000 | 25% | 50% percentile | 170 | 2,334.1 | 6.0% |
| 100,000 | 25% | 60% percentile | 170 | 2,796.3 | 7.2% |
| 100,000 | 33% | 40% percentile | 225 | 1,984.6 | 5.1% |
| 100,000 | 33% | 50% percentile | 225 | 2,699.8 | 7.0% |
| 100,000 | 33% | 60% percentile | 225 | 3,309.6 | 8.6% |
| 200,000 | 20% | 40% percentile | 125 | 1,716.4 | 4.4% |
| 200,000 | 20% | 50% percentile | 125 | 2,123.7 | 5.5% |
| 200,000 | 20% | 60% percentile | 125 | 2,540.1 | 6.6% |
| 200,000 | 25% | 40% percentile | 156 | 1,979.7 | 5.1% |
| 200,000 | 25% | 50% percentile | 156 | 2,508.6 | 6.5% |
| 200,000 | 25% | 60% percentile | 156 | 3,049.5 | 7.9% |
| 200,000 | 33% | 40% percentile | 205 | 2,229.9 | 5.8% |
| 200,000 | 33% | 50% percentile | 205 | 2,959.4 | 7.7% |
| 200,000 | 33% | 60% percentile | 205 | 3,705.5 | 9.6% |

The direction never changes: under every combination tested, lifting low-usage districts adds volume. The size depends on how ambitious the target is (lifting to the 40th percentile adds far less than to the 60th), so the headline should be read as an order of magnitude, not a forecast.
