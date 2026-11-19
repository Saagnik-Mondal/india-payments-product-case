-- Q7. Where is the engagement gap? Districts (with 100k+ registered users) in the bottom quarter
-- of transactions per user. How many extra transactions per quarter would there be if each
-- reached the median district? Grouped by state.
WITH d AS (
    SELECT state, district, users, txns * 1.0 / users AS tpu
    FROM district_latest
    WHERE users >= 100000 AND txns > 0
),
q AS (
    SELECT quantile_cont(tpu, 0.25) AS p25, quantile_cont(tpu, 0.5) AS p50 FROM d
),
gap AS (
    SELECT d.state, d.district, d.users, d.tpu, (q.p50 - d.tpu) * d.users AS extra_txns
    FROM d CROSS JOIN q WHERE d.tpu < q.p25
)
SELECT
    state,
    count(*) AS districts_in_bottom_quarter,
    round(sum(users) / 1e6, 1) AS registered_users_m,
    round(sum(extra_txns) / 1e6, 1) AS extra_txns_m_per_quarter_if_raised_to_median
FROM gap
GROUP BY state
ORDER BY sum(extra_txns) DESC, state;
