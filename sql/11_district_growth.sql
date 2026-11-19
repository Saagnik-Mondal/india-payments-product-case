-- Q11. How much does district engagement move in a year? Used to size a district-level experiment.
-- Districts with 100k+ registered users in both the latest quarter and the same quarter a year earlier.
WITH prev AS (
    SELECT t.state, t.district, t.count AS txns, u.registered_users AS users
    FROM district_txn t
    JOIN district_users u
        ON u.state = t.state AND u.district = t.district AND u.year = t.year AND u.quarter = t.quarter
    JOIN latest l ON t.year = l.year - 1 AND t.quarter = l.quarter
)
SELECT
    c.state,
    c.district,
    c.users,
    round(c.txns * 1.0 / c.users, 2) AS txns_per_user,
    round(p.txns * 1.0 / p.users, 2) AS txns_per_user_year_ago,
    round(100 * ((c.txns * 1.0 / c.users) / (p.txns * 1.0 / p.users) - 1), 1) AS txns_per_user_growth_yoy_pct
FROM district_latest c
JOIN prev p ON p.state = c.state AND p.district = c.district
WHERE c.users >= 100000 AND p.users >= 100000 AND p.txns > 0 AND c.txns > 0
ORDER BY c.state, c.district;
