-- Q3. What are people paying for? Share of transactions by category over time.
-- P2P = person to person, Retail = merchant payments, Utility = bills and recharges.
SELECT
    year, quarter, category, count,
    round(100.0 * count / sum(count) OVER (PARTITION BY year, quarter), 1) AS share_pct
FROM national_category
ORDER BY year, quarter, category;
