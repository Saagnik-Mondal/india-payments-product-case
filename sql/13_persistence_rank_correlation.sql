-- Q13. One-number version of Q12: rank correlation between a district's transactions per user
-- three years ago and now (1 = same order, 0 = unrelated).
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
ranked AS (
    SELECT rank() OVER (ORDER BY tpu_then, state, district) AS r_then,
           rank() OVER (ORDER BY tpu_now, state, district) AS r_now
    FROM j
)
SELECT count(*) AS districts, round(corr(r_then, r_now), 2) AS rank_correlation FROM ranked;
