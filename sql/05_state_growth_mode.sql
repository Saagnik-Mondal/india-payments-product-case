-- Q5. Is each state growing by adding users or by deepening use? Latest quarter vs a year earlier.
WITH cur AS (
    SELECT state, txns, users FROM state_latest
),
prev AS (
    SELECT t.state, t.count AS txns, u.registered_users AS users
    FROM state_txn t
    JOIN state_users u ON u.state = t.state AND u.year = t.year AND u.quarter = t.quarter
    JOIN latest l ON t.year = l.year - 1 AND t.quarter = l.quarter
),
g AS (
    SELECT cur.state,
           cur.txns * 1.0 / prev.txns - 1 AS g_txn,
           cur.users * 1.0 / prev.users - 1 AS g_users,
           (cur.txns * 1.0 / cur.users) / (prev.txns * 1.0 / prev.users) - 1 AS g_tpu
    FROM cur JOIN prev ON prev.state = cur.state
)
SELECT
    state,
    round(100 * g_txn, 1) AS txn_growth_yoy_pct,
    round(100 * g_users, 1) AS user_growth_yoy_pct,
    round(100 * g_tpu, 1) AS engagement_growth_yoy_pct,
    round(100 * ln(1 + g_users) / ln(1 + g_txn), 0) AS pct_of_growth_from_more_users
FROM g
ORDER BY txn_growth_yoy_pct DESC, state;
