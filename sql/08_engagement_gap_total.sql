-- Q8. Total size of the engagement gap in Q7, against all transactions in the quarter.
WITH d AS (
    SELECT district, users, txns * 1.0 / users AS tpu
    FROM district_latest
    WHERE users >= 100000 AND txns > 0
),
q AS (
    SELECT quantile_cont(tpu, 0.25) AS p25, quantile_cont(tpu, 0.5) AS p50 FROM d
),
gap AS (
    SELECT d.users, (q.p50 - d.tpu) * d.users AS extra_txns
    FROM d CROSS JOIN q WHERE d.tpu < q.p25
)
SELECT
    (SELECT count(*) FROM d) AS districts_considered,
    (SELECT count(*) FROM gap) AS districts_in_bottom_quarter,
    round((SELECT p25 FROM q), 1) AS p25_txns_per_user,
    round((SELECT p50 FROM q), 1) AS median_txns_per_user,
    round((SELECT sum(users) FROM gap) / 1e6, 1) AS users_in_gap_m,
    round((SELECT sum(extra_txns) FROM gap) / 1e6, 1) AS extra_txns_m_per_quarter,
    round(100.0 * (SELECT sum(extra_txns) FROM gap) / (SELECT sum(txns) FROM district_latest), 1) AS extra_pct_of_all_txns;
