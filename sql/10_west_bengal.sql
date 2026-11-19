-- Q10. Spotlight on West Bengal: districts compared with the national median district.
-- North Bengal districts are listed explicitly; the rest of the state is "South Bengal".
WITH nat AS (
    SELECT quantile_cont(txns * 1.0 / users, 0.5) AS median_tpu,
           quantile_cont(1000.0 * merchants / users, 0.5) AS median_mpk
    FROM district_latest
    WHERE users >= 100000 AND txns > 0
)
SELECT
    d.district,
    CASE WHEN d.district IN (
        'alipurduar district', 'cooch behar district', 'dakshin dinajpur district', 'darjeeling district',
        'jalpaiguri district', 'kalimpong district', 'malda district', 'uttar dinajpur district'
    ) THEN 'North Bengal' ELSE 'South Bengal' END AS region,
    d.users,
    d.txns,
    round(d.txns * 1.0 / d.users, 1) AS txns_per_user,
    round(nat.median_tpu, 1) AS national_median_txns_per_user,
    round(1000.0 * d.merchants / d.users, 1) AS merchants_per_1000_users,
    round(nat.median_mpk, 1) AS national_median_merchants_per_1000_users
FROM district_latest d
CROSS JOIN nat
WHERE d.state = 'west bengal'
ORDER BY txns_per_user DESC, d.district;
