# Changelog

## 0.3.0 - 2026-11-19

### Added
- Persistence check: low-usage districts do not catch up on their own. District ranks in 2023 and 2026 correlate at 0.96, and 83.9% of the lowest quarter in 2023 is still in the lowest quarter (`sql/12_persistence.sql`, `sql/13_persistence_rank_correlation.sql`). Closes #1.

## 0.2.0 - 2026-11-19

### Added
- Robustness check on the headline engagement-gap estimate: 27 combinations of the registered-user floor, the share of districts lifted and the target percentile (`analysis/robustness.py`, `results/robustness.md`). The estimate ranges from 3.8% to 9.6% of volume; the headline 6.0% sits near the middle.
- The check runs in CI with the rest of the analysis.

## 0.1.0 - 2026-11-19

First release: 11 SQL queries over 34 quarters of PhonePe Pulse data, charts, a north-star metric, prioritised recommendations, experiment sizing, and CI that re-runs everything and checks the results match.
