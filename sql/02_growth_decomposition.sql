-- Q2. Is growth coming from more users or from users doing more?
-- Compares each Q2 with the previous year's Q2. Transactions = users x transactions per user,
-- so log-growth splits exactly into a users part and an engagement part.
WITH n AS (
    SELECT year, quarter, txns, users, txns * 1.0 / users AS tpu FROM national WHERE quarter = 2
),
g AS (
    SELECT cur.year,
           cur.txns / prev.txns - 1 AS g_txn,
           cur.users * 1.0 / prev.users - 1 AS g_users,
           cur.tpu / prev.tpu - 1 AS g_tpu
    FROM n cur JOIN n prev ON prev.year = cur.year - 1
)
SELECT
    year,
    round(100 * g_txn, 1) AS txn_growth_pct,
    round(100 * g_users, 1) AS users_growth_pct,
    round(100 * g_tpu, 1) AS engagement_growth_pct,
    round(100 * ln(1 + g_users) / ln(1 + g_txn), 0) AS pct_of_growth_from_more_users,
    round(100 * ln(1 + g_tpu) / ln(1 + g_txn), 0) AS pct_of_growth_from_more_usage
FROM g
ORDER BY year;
