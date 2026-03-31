-- ============================================================================
-- SUPERSTORE SALES ANALYSIS - SQL QUERIES
-- ============================================================================
-- Professional SQL queries for the Superstore dataset analysis
-- Database: Superstore
-- Last Updated: 2026-03-31
-- ============================================================================


-- ============================================================================
-- QUERY 1: TOTAL REVENUE
-- ============================================================================
-- Calculate the total revenue across all sales
SELECT 
    SUM(sales) AS total_revenue
FROM 
    superstore_sales
WHERE 
    sales > 0
    AND order_date IS NOT NULL;


-- ============================================================================
-- QUERY 2: TOTAL PROFIT
-- ============================================================================
-- Calculate the total profit and profit margin
SELECT 
    SUM(profit) AS total_profit,
    SUM(sales) AS total_sales,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percentage
FROM 
    superstore_sales
WHERE 
    sales > 0
    AND profit IS NOT NULL;


-- ============================================================================
-- QUERY 3: REVENUE BY REGION
-- ============================================================================
-- Analyze revenue distribution across regions with rankings
SELECT 
    region,
    COUNT(DISTINCT order_id) AS number_of_orders,
    COUNT(DISTINCT customer_id) AS number_of_customers,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(AVG(sales), 2) AS average_order_value,
    ROUND(SUM(profit), 2) AS total_profit,
    RANK() OVER (ORDER BY SUM(sales) DESC) AS revenue_rank
FROM 
    superstore_sales
WHERE 
    sales > 0
GROUP BY 
    region
ORDER BY 
    total_revenue DESC;


-- ============================================================================
-- QUERY 4: TOP 20 CUSTOMERS BY REVENUE
-- ============================================================================
-- Identify the most valuable customers by lifetime revenue
SELECT 
    customer_id,
    customer_name,
    COUNT(DISTINCT order_id) AS number_of_orders,
    ROUND(SUM(sales), 2) AS lifetime_revenue,
    ROUND(SUM(profit), 2) AS lifetime_profit,
    ROUND(AVG(sales), 2) AS average_order_value,
    MAX(order_date) AS last_order_date
FROM 
    superstore_sales
WHERE 
    sales > 0
GROUP BY 
    customer_id,
    customer_name
ORDER BY 
    lifetime_revenue DESC
LIMIT 20;


-- ============================================================================
-- QUERY 5: CATEGORY PERFORMANCE ANALYSIS
-- ============================================================================
-- Detailed performance metrics by product category
SELECT 
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_percentage,
    ROUND(AVG(sales), 2) AS average_order_value,
    ROUND(SUM(quantity), 0) AS units_sold
FROM 
    superstore_sales
WHERE 
    sales > 0
GROUP BY 
    category,
    sub_category
ORDER BY 
    total_sales DESC;


-- ============================================================================
-- QUERY 6: MONTHLY SALES TRENDS
-- ============================================================================
-- Track sales performance and trends by month and year
SELECT 
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    TO_CHAR(order_date, 'YYYY-MM') AS year_month,
    TO_CHAR(order_date, 'Month') AS month_name,
    COUNT(DISTINCT order_id) AS number_of_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales), 2) AS monthly_revenue,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin,
    ROUND(AVG(sales), 2) AS average_order_value
FROM 
    superstore_sales
WHERE 
    sales > 0
    AND order_date IS NOT NULL
GROUP BY 
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date),
    TO_CHAR(order_date, 'YYYY-MM'),
    TO_CHAR(order_date, 'Month')
ORDER BY 
    year DESC,
    month DESC;


-- ============================================================================
-- QUERY 7: CUSTOMER SEGMENTATION BY SPENDING
-- ============================================================================
-- Segment customers into high, medium, and low value categories
SELECT 
    CASE 
        WHEN total_revenue >= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_revenue) 
                               FROM (SELECT SUM(sales) AS total_revenue FROM superstore_sales GROUP BY customer_id))
        THEN 'High Value'
        WHEN total_revenue >= (SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_revenue) 
                               FROM (SELECT SUM(sales) AS total_revenue FROM superstore_sales GROUP BY customer_id))
        THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS number_of_customers,
    ROUND(AVG(total_revenue), 2) AS average_revenue,
    ROUND(MIN(total_revenue), 2) AS min_revenue,
    ROUND(MAX(total_revenue), 2) AS max_revenue
FROM 
    (SELECT 
        customer_id,
        SUM(sales) AS total_revenue
    FROM 
        superstore_sales
    GROUP BY 
        customer_id)
GROUP BY 
    customer_segment
ORDER BY 
    CASE 
        WHEN customer_segment = 'High Value' THEN 1
        WHEN customer_segment = 'Medium Value' THEN 2
        ELSE 3
    END;


-- ============================================================================
-- QUERY 8: REGIONAL PERFORMANCE COMPARISON
-- ============================================================================
-- Compare performance metrics across regions
SELECT 
    region,
    category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin
FROM 
    superstore_sales
WHERE 
    sales > 0
GROUP BY 
    region,
    category
ORDER BY 
    region,
    revenue DESC;


-- ============================================================================
-- QUERY 9: YEAR-OVER-YEAR GROWTH ANALYSIS
-- ============================================================================
-- Calculate YoY growth rates for revenue and profit
WITH yearly_metrics AS (
    SELECT 
        EXTRACT(YEAR FROM order_date) AS year,
        ROUND(SUM(sales), 2) AS annual_revenue,
        ROUND(SUM(profit), 2) AS annual_profit
    FROM 
        superstore_sales
    WHERE 
        sales > 0
    GROUP BY 
        EXTRACT(YEAR FROM order_date)
)
SELECT 
    year,
    annual_revenue,
    annual_profit,
    ROUND((annual_revenue - LAG(annual_revenue) OVER (ORDER BY year)) / 
          LAG(annual_revenue) OVER (ORDER BY year) * 100, 2) AS revenue_growth_percentage,
    ROUND((annual_profit - LAG(annual_profit) OVER (ORDER BY year)) / 
          LAG(annual_profit) OVER (ORDER BY year) * 100, 2) AS profit_growth_percentage
FROM 
    yearly_metrics
ORDER BY 
    year ASC;


-- ============================================================================
-- QUERY 10: PRODUCT PERFORMANCE INSIGHTS
-- ============================================================================
-- Identify top and bottom performing products
SELECT 
    product_name,
    category,
    COUNT(DISTINCT order_id) AS times_ordered,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit), 2) AS average_profit_per_sale,
    ROUND(SUM(quantity), 0) AS units_sold,
    RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM 
    superstore_sales
WHERE 
    sales > 0
GROUP BY 
    product_name,
    category
ORDER BY 
    total_profit DESC
LIMIT 25;


-- ============================================================================
-- NOTE ON DATABASE SETUP
-- ============================================================================
-- To use these queries, ensure your database contains a table with the following structure:
-- 
-- CREATE TABLE superstore_sales (
--     order_id VARCHAR(50),
--     order_date DATE,
--     ship_date DATE,
--     ship_mode VARCHAR(50),
--     customer_id VARCHAR(50),
--     customer_name VARCHAR(100),
--     segment VARCHAR(50),
--     region VARCHAR(50),
--     state VARCHAR(50),
--     postal_code VARCHAR(20),
--     country VARCHAR(50),
--     market VARCHAR(50),
--     category VARCHAR(50),
--     sub_category VARCHAR(50),
--     product_name VARCHAR(255),
--     sales DECIMAL(10, 2),
--     quantity INT,
--     discount DECIMAL(5, 2),
--     profit DECIMAL(10, 2),
--     PRIMARY KEY (order_id)
-- );
--
-- Adjust table and column names as necessary to match your actual schema.
-- ============================================================================
