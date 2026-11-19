-- Q12. Is low engagement persistent? Districts grouped by transactions per user three years ago
-- (1 = lowest quarter) and where they are now. Districts with 100k+ registered users in both periods.
WITH prev AS (
    SELECT t.state, t.district, t.count AS txns, u.registered_users AS users
    FROM district_txn t
    JOIN district_users u
        ON u.state = t.state AND u.district = t.district AND u.year = t.year AND u.quarter = t.quarter
    JOIN latest l ON t.year = l.year - 3 AND t.quarter = l.quarter
),
j AS (
    SELECT c.state, c.district,
           p.txns * 1.0 / p.users AS tpu_then,
           c.txns * 1.0 / c.users AS tpu_now
    FROM district_latest c
    JOIN prev p ON p.state = c.state AND p.district = c.district
    WHERE c.users >= 100000 AND p.users >= 100000 AND p.txns > 0 AND c.txns > 0
),
r AS (
    SELECT *,
           ntile(4) OVER (ORDER BY tpu_then, state, district) AS q_then,
           ntile(4) OVER (ORDER BY tpu_now, state, district) AS q_now
    FROM j
)
SELECT
    q_then AS quarter_three_years_ago,
    count(*) AS districts,
    round(avg(tpu_then), 1) AS avg_txns_per_user_then,
    round(avg(tpu_now), 1) AS avg_txns_per_user_now,
    round(avg(tpu_now / tpu_then), 2) AS avg_growth_multiple,
    round(100.0 * sum(CASE WHEN q_now = 1 THEN 1 ELSE 0 END) / count(*), 1) AS pct_still_in_lowest_quarter,
    round(100.0 * sum(CASE WHEN q_now = 4 THEN 1 ELSE 0 END) / count(*), 1) AS pct_now_in_highest_quarter
FROM r
GROUP BY q_then
ORDER BY q_then;
