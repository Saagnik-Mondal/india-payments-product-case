# Changelog

## 0.2.0 - 2026-11-19

### Added
- Robustness check on the headline engagement-gap estimate: 27 combinations of the registered-user floor, the share of districts lifted and the target percentile (`analysis/robustness.py`, `results/robustness.md`). The estimate ranges from 3.8% to 9.6% of volume; the headline 6.0% sits near the middle.
- The check runs in CI with the rest of the analysis.

## 0.1.0 - 2026-11-19

First release: 11 SQL queries over 34 quarters of PhonePe Pulse data, charts, a north-star metric, prioritised recommendations, experiment sizing, and CI that re-runs everything and checks the results match.
