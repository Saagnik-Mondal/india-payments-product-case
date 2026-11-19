-- Q4. Which states are deep, and which are wide but shallow? Latest quarter by state.
WITH cat AS (
    SELECT c.state,
           sum(CASE WHEN category = 'Retail' THEN count END) * 1.0 / sum(count) AS retail_share,
           sum(CASE WHEN category = 'P2P' THEN count END) * 1.0 / sum(count) AS p2p_share
    FROM state_category c
    JOIN latest l ON c.year = l.year AND c.quarter = l.quarter
    GROUP BY c.state
)
SELECT
    s.state,
    s.users,
    s.txns,
    round(s.txns * 1.0 / s.users, 1) AS txns_per_user,
    round(1000.0 * s.merchants / s.users, 1) AS merchants_per_1000_users,
    round(s.amount / s.txns, 0) AS avg_ticket_inr,
    round(100 * cat.retail_share, 1) AS retail_pct,
    round(100 * cat.p2p_share, 1) AS p2p_pct,
    round(100.0 * s.users / sum(s.users) OVER (), 1) AS pct_of_all_users,
    round(100.0 * s.txns / sum(s.txns) OVER (), 1) AS pct_of_all_txns,
    rank() OVER (ORDER BY s.txns * 1.0 / s.users DESC, s.state) AS rank_txns_per_user
FROM state_latest s
LEFT JOIN cat ON cat.state = s.state
ORDER BY txns_per_user DESC, s.state;
