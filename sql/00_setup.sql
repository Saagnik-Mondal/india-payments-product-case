-- Base tables and shared views. {DATA} is replaced with data/tables by analysis/run.py.
-- Definitions used throughout:
--   transactions  count of payments in the quarter
--   users         registered users at the end of the quarter (a stock, not "active" users)
--   merchants     registered merchants at the end of the quarter
--   txns per user transactions in the quarter divided by registered users (an engagement proxy)
CREATE OR REPLACE VIEW national_category AS SELECT * FROM read_csv_auto('{DATA}/national_category.csv');
CREATE OR REPLACE VIEW state_category AS SELECT * FROM read_csv_auto('{DATA}/state_category.csv');
CREATE OR REPLACE VIEW state_txn AS SELECT * FROM read_csv_auto('{DATA}/state_txn.csv');
CREATE OR REPLACE VIEW district_txn AS SELECT * FROM read_csv_auto('{DATA}/district_txn.csv');
CREATE OR REPLACE VIEW national_users AS SELECT * FROM read_csv_auto('{DATA}/national_users.csv');
CREATE OR REPLACE VIEW state_users AS SELECT * FROM read_csv_auto('{DATA}/state_users.csv');
CREATE OR REPLACE VIEW district_users AS SELECT * FROM read_csv_auto('{DATA}/district_users.csv');
CREATE OR REPLACE VIEW state_merchants AS SELECT * FROM read_csv_auto('{DATA}/state_merchants.csv');
CREATE OR REPLACE VIEW district_merchants AS SELECT * FROM read_csv_auto('{DATA}/district_merchants.csv');

CREATE OR REPLACE VIEW national AS
SELECT t.year, t.quarter, t.txns, t.amount, u.registered_users AS users, m.merchants
FROM (SELECT year, quarter, sum(count) AS txns, sum(amount) AS amount FROM state_txn GROUP BY year, quarter) t
JOIN national_users u ON u.year = t.year AND u.quarter = t.quarter
LEFT JOIN (SELECT year, quarter, sum(registered_merchants) AS merchants FROM state_merchants GROUP BY year, quarter) m
    ON m.year = t.year AND m.quarter = t.quarter;

CREATE OR REPLACE VIEW latest AS
SELECT year, quarter FROM national ORDER BY year DESC, quarter DESC LIMIT 1;

CREATE OR REPLACE VIEW state_latest AS
SELECT t.state, t.count AS txns, t.amount, u.registered_users AS users, coalesce(m.registered_merchants, 0) AS merchants
FROM state_txn t
JOIN latest l ON t.year = l.year AND t.quarter = l.quarter
JOIN state_users u ON u.state = t.state AND u.year = t.year AND u.quarter = t.quarter
LEFT JOIN state_merchants m ON m.state = t.state AND m.year = t.year AND m.quarter = t.quarter;

CREATE OR REPLACE VIEW district_latest AS
SELECT t.state, t.district, t.count AS txns, t.amount, u.registered_users AS users, coalesce(m.registered_merchants, 0) AS merchants
FROM district_txn t
JOIN latest l ON t.year = l.year AND t.quarter = l.quarter
JOIN district_users u ON u.state = t.state AND u.district = t.district AND u.year = t.year AND u.quarter = t.quarter
LEFT JOIN district_merchants m ON m.state = t.state AND m.district = t.district AND m.year = t.year AND m.quarter = t.quarter;
