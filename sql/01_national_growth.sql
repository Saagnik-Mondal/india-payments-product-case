-- Q1. How fast is the platform growing, and how deeply do people use it?
-- Quarterly transactions, registered users, merchants, transactions per user and average ticket,
-- with year-over-year growth.
WITH n AS (
    SELECT year, quarter, year * 4 + quarter AS idx, txns, amount, users, merchants,
           txns * 1.0 / users AS txns_per_user
    FROM national
)
SELECT
    cur.year, cur.quarter,
    round(cur.txns / 1e9, 3) AS transactions_bn,
    round(cur.amount / 1e12, 2) AS value_trillion_inr,
    round(cur.users / 1e6, 1) AS registered_users_m,
    round(cur.merchants / 1e6, 2) AS registered_merchants_m,
    round(cur.txns_per_user, 1) AS txns_per_user,
    round(cur.amount / cur.txns, 0) AS avg_ticket_inr,
    round(100 * (cur.txns / prev.txns - 1), 1) AS txn_growth_yoy_pct,
    round(100 * (cur.users * 1.0 / prev.users - 1), 1) AS user_growth_yoy_pct,
    round(100 * (cur.txns_per_user / prev.txns_per_user - 1), 1) AS engagement_growth_yoy_pct
FROM n cur
LEFT JOIN n prev ON prev.idx = cur.idx - 4
ORDER BY cur.year, cur.quarter;
