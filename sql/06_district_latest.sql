-- Q6. District view, latest quarter (all districts). Used for the engagement-gap sizing and charts.
SELECT
    state, district, users, txns, merchants,
    round(txns * 1.0 / users, 1) AS txns_per_user,
    round(1000.0 * merchants / users, 1) AS merchants_per_1000_users,
    round(amount / txns, 0) AS avg_ticket_inr
FROM district_latest
WHERE users > 0 AND txns > 0
ORDER BY txns_per_user DESC, state, district;
