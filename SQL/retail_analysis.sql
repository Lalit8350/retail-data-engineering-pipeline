
-- ==========================================
-- Retail Data Engineering Pipeline
-- SQL Analysis Queries
-- ==========================================

-- Query 1: Top 10 countries by total line amount
SELECT
    country,
    COUNT(*) AS transaction_lines,
    ROUND(SUM(line_amount), 2) AS total_line_amount
FROM retail_transactions
GROUP BY country
ORDER BY total_line_amount DESC
LIMIT 10;


-- Query 2: Monthly sales analysis
SELECT
    DATE_TRUNC('month', invoice_date)::date AS sales_month,
    COUNT(*) AS transaction_lines,
    COUNT(DISTINCT invoice_no) AS invoice_count,
    ROUND(SUM(line_amount), 2) AS net_line_amount
FROM retail_transactions
WHERE is_cancellation = FALSE
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY sales_month;


-- Query 3: Top 10 products by positive line amount
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT invoice_no) AS invoice_count,
    ROUND(SUM(line_amount), 2) AS total_line_amount
FROM retail_transactions
WHERE is_cancellation = FALSE
  AND quantity > 0
  AND unit_price > 0
GROUP BY stock_code, description
ORDER BY total_line_amount DESC
LIMIT 10;


-- 4. Investigate large manual cancellation records
SELECT
    invoice_no,
    invoice_date,
    customer_id,
    country,
    quantity,
    unit_price,
    line_amount
FROM retail_transactions
WHERE stock_code = 'M'
  AND is_cancellation = TRUE
  AND ABS(line_amount) > 1000
ORDER BY ABS(line_amount) DESC;


-- 5. Find the top merchandise product in each country
WITH country_product_sales AS (
    SELECT
        country,
        stock_code,
        description,
        ROUND(SUM(line_amount), 2) AS total_line_amount
    FROM retail_transaction_classified
    WHERE is_cancellation = FALSE
      AND quantity > 0
      AND unit_price > 0
      AND item_category = 'MERCHANDISE_OR_OTHER'
    GROUP BY country, stock_code, description
),
ranked_products AS (
    SELECT
        country,
        stock_code,
        description,
        total_line_amount,
        ROW_NUMBER() OVER (
            PARTITION BY country
            ORDER BY total_line_amount DESC, stock_code, description
        ) AS product_rank
    FROM country_product_sales
)
SELECT
    country,
    stock_code,
    description,
    total_line_amount
FROM ranked_products
WHERE product_rank = 1
ORDER BY total_line_amount DESC
LIMIT 15;


