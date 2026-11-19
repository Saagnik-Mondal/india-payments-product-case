-- Q9. How concentrated is usage? Share of transactions from the top 5 states and the top
-- 10% of districts, each Q2 (and the latest quarter is a Q2).
WITH s AS (
    SELECT year, quarter, count,
           rank() OVER (PARTITION BY year, quarter ORDER BY count DESC, state) AS rk
    FROM state_txn
),
d AS (
    SELECT year, quarter, count,
           ntile(10) OVER (PARTITION BY year, quarter ORDER BY count DESC, state, district) AS decile
    FROM district_txn
)
SELECT
    s.year,
    round(100.0 * sum(CASE WHEN s.rk <= 5 THEN s.count END) / sum(s.count), 1) AS top5_states_share_pct,
    (SELECT round(100.0 * sum(CASE WHEN d.decile = 1 THEN d.count END) / sum(d.count), 1)
     FROM d WHERE d.year = s.year AND d.quarter = 2) AS top10pct_districts_share_pct
FROM s
WHERE s.quarter = 2
GROUP BY s.year
ORDER BY s.year;
