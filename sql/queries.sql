-- ============================================================================
-- SUPERSTORE SALES ANALYSIS - PRODUCTION SQL QUERIES
-- ============================================================================
-- Comprehensive analytics queries for business intelligence
-- Last Updated: March 31, 2026
-- ============================================================================

-- ============================================================================
-- QUERY 1: EXECUTIVE SUMMARY - KEY METRICS
-- ============================================================================
-- Overview of business performance across all dimensions
SELECT 
    COUNT(DISTINCT ORDER_ID) AS total_orders,
    COUNT(DISTINCT CUSTOMER_ID) AS unique_customers,
    COUNT(DISTINCT REGION) AS regions,
    COUNT(DISTINCT CATEGORY) AS categories,
    ROUND(SUM(SALES), 2) AS total_revenue,
    ROUND(SUM(PROFIT), 2) AS total_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(SALES), 2) AS avg_order_value,
    ROUND(SUM(QUANTITY), 0) AS units_sold
FROM 
    superstore_sales
WHERE 
    SALES > 0 AND ORDER_DATE IS NOT NULL;


-- ============================================================================
-- QUERY 2: REVENUE BY REGION (RANKED)
-- ============================================================================
-- Regional performance analysis with market share and rankings
SELECT 
    REGION,
    COUNT(DISTINCT ORDER_ID) AS order_count,
    COUNT(DISTINCT CUSTOMER_ID) AS customer_count,
    ROUND(SUM(SALES), 2) AS region_revenue,
    ROUND(AVG(SALES), 2) AS avg_order_value,
    ROUND(SUM(PROFIT), 2) AS region_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(SALES) / (SELECT SUM(SALES) FROM superstore_sales) * 100, 2) AS market_share_pct,
    RANK() OVER (ORDER BY SUM(SALES) DESC) AS revenue_rank
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    REGION
ORDER BY 
    region_revenue DESC;


-- ============================================================================
-- QUERY 3: TOP 20 CUSTOMERS BY LIFETIME VALUE
-- ============================================================================
-- VIP customer identification for retention and loyalty programs
SELECT 
    CUSTOMER_ID,
    CUSTOMER_NAME,
    COUNT(DISTINCT ORDER_ID) AS transaction_count,
    ROUND(SUM(SALES), 2) AS lifetime_revenue,
    ROUND(SUM(PROFIT), 2) AS lifetime_profit,
    ROUND(AVG(SALES), 2) AS avg_order_value,
    ROUND(SUM(QUANTITY), 0) AS total_units,
    MAX(ORDER_DATE) AS last_purchase_date,
    MIN(ORDER_DATE) AS first_purchase_date,
    DATEDIFF(MAX(ORDER_DATE), MIN(ORDER_DATE)) AS customer_tenure_days,
    RANK() OVER (ORDER BY SUM(SALES) DESC) AS customer_rank
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    CUSTOMER_ID, CUSTOMER_NAME
ORDER BY 
    lifetime_revenue DESC
LIMIT 20;


-- ============================================================================
-- QUERY 4: CATEGORY PERFORMANCE MATRIX
-- ============================================================================
-- Profitability analysis by category and subcategory
SELECT 
    CATEGORY,
    SUB_CATEGORY,
    COUNT(DISTINCT ORDER_ID) AS orders,
    COUNT(DISTINCT CUSTOMER_ID) AS unique_customers,
    ROUND(SUM(SALES), 2) AS category_revenue,
    ROUND(SUM(PROFIT), 2) AS category_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(QUANTITY), 0) AS units_sold,
    ROUND(AVG(SALES), 2) AS avg_order_value,
    CASE 
        WHEN SUM(PROFIT) / SUM(SALES) >= 0.20 THEN 'High Margin'
        WHEN SUM(PROFIT) / SUM(SALES) >= 0.10 THEN 'Medium Margin'
        ELSE 'Low Margin'
    END AS margin_classification
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    CATEGORY, SUB_CATEGORY
ORDER BY 
    category_revenue DESC;


-- ============================================================================
-- QUERY 5: MONTHLY SALES TRENDS & SEASONALITY
-- ============================================================================
-- Year-over-year monthly performance for forecasting
SELECT 
    YEAR(ORDER_DATE) AS sales_year,
    MONTH(ORDER_DATE) AS sales_month,
    FORMAT(ORDER_DATE, 'yyyy-MM') AS year_month,
    FORMAT(ORDER_DATE, 'MMMM') AS month_name,
    COUNT(DISTINCT ORDER_ID) AS monthly_orders,
    COUNT(DISTINCT CUSTOMER_ID) AS monthly_customers,
    ROUND(SUM(SALES), 2) AS monthly_revenue,
    ROUND(SUM(PROFIT), 2) AS monthly_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS margin_pct,
    ROUND(SUM(QUANTITY), 0) AS units,
    ROUND(AVG(SALES), 2) AS avg_order_value
FROM 
    superstore_sales
WHERE 
    SALES > 0 AND ORDER_DATE IS NOT NULL
GROUP BY 
    YEAR(ORDER_DATE), MONTH(ORDER_DATE), FORMAT(ORDER_DATE, 'yyyy-MM'), FORMAT(ORDER_DATE, 'MMMM')
ORDER BY 
    sales_year DESC, sales_month DESC;


-- ============================================================================
-- QUERY 6: CUSTOMER SEGMENT ANALYSIS (RFM MODEL)
-- ============================================================================
-- Recency, Frequency, Monetary segmentation for targeted marketing
WITH customer_metrics AS (
    SELECT 
        CUSTOMER_ID,
        CUSTOMER_NAME,
        DATEDIFF(DAY, MAX(ORDER_DATE), (SELECT MAX(ORDER_DATE) FROM superstore_sales)) AS recency_days,
        COUNT(DISTINCT ORDER_ID) AS frequency,
        ROUND(SUM(SALES), 2) AS monetary_value
    FROM 
        superstore_sales
    WHERE 
        SALES > 0
    GROUP BY 
        CUSTOMER_ID, CUSTOMER_NAME
)
SELECT 
    CUSTOMER_ID,
    CUSTOMER_NAME,
    recency_days,
    frequency,
    monetary_value,
    CASE 
        WHEN recency_days <= 30 AND frequency >= 5 AND monetary_value >= 1000 THEN 'Champions'
        WHEN recency_days <= 60 AND frequency >= 3 AND monetary_value >= 500 THEN 'Loyal Customers'
        WHEN recency_days <= 90 AND frequency >= 2 THEN 'Promising'
        WHEN recency_days > 180 THEN 'At Risk'
        ELSE 'Emerging'
    END AS customer_segment
FROM 
    customer_metrics
ORDER BY 
    monetary_value DESC;


-- ============================================================================
-- QUERY 7: DISCOUNT IMPACT ANALYSIS
-- ============================================================================
-- Understanding how discounts affect profitability
SELECT 
    CASE 
        WHEN DISCOUNT = 0 THEN 'No Discount'
        WHEN DISCOUNT <= 0.10 THEN '0-10% Discount'
        WHEN DISCOUNT <= 0.20 THEN '10-20% Discount'
        ELSE '> 20% Discount'
    END AS discount_bucket,
    COUNT(DISTINCT ORDER_ID) AS order_count,
    COUNT(DISTINCT CUSTOMER_ID) AS customer_count,
    ROUND(AVG(SALES), 2) AS avg_order_value,
    ROUND(SUM(SALES), 2) AS total_sales,
    ROUND(SUM(PROFIT), 2) AS total_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(PROFIT), 2) AS avg_profit_per_order
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    CASE 
        WHEN DISCOUNT = 0 THEN 'No Discount'
        WHEN DISCOUNT <= 0.10 THEN '0-10% Discount'
        WHEN DISCOUNT <= 0.20 THEN '10-20% Discount'
        ELSE '> 20% Discount'
    END
ORDER BY 
    CASE 
        WHEN discount_bucket = 'No Discount' THEN 1
        WHEN discount_bucket = '0-10% Discount' THEN 2
        WHEN discount_bucket = '10-20% Discount' THEN 3
        ELSE 4
    END;


-- ============================================================================
-- QUERY 8: GEOGRAPHIC PERFORMANCE (STATE LEVEL)
-- ============================================================================
-- State-by-state performance for insights and targeted strategies
SELECT 
    REGION,
    STATE,
    COUNT(DISTINCT ORDER_ID) AS state_orders,
    COUNT(DISTINCT CUSTOMER_ID) AS state_customers,
    ROUND(SUM(SALES), 2) AS state_revenue,
    ROUND(SUM(PROFIT), 2) AS state_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    RANK() OVER (PARTITION BY REGION ORDER BY SUM(SALES) DESC) AS state_rank_in_region
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    REGION, STATE
ORDER BY 
    REGION, state_revenue DESC;


-- ============================================================================
-- QUERY 9: PRODUCT PERFORMANCE RANKINGS
-- ============================================================================
-- Top and bottom performing products by profitability
SELECT 
    PRODUCT_NAME,
    CATEGORY,
    SUB_CATEGORY,
    COUNT(DISTINCT ORDER_ID) AS times_ordered,
    ROUND(SUM(QUANTITY), 0) AS units_sold,
    ROUND(SUM(SALES), 2) AS total_sales,
    ROUND(SUM(PROFIT), 2) AS total_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(PROFIT), 2) AS avg_profit_per_sale,
    RANK() OVER (ORDER BY SUM(PROFIT) DESC) AS profit_rank,
    RANK() OVER (ORDER BY COUNT(DISTINCT ORDER_ID) DESC) AS popularity_rank
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    PRODUCT_NAME, CATEGORY, SUB_CATEGORY
ORDER BY 
    total_profit DESC;


-- ============================================================================
-- QUERY 10: YEAR-OVER-YEAR GROWTH ANALYSIS
-- ============================================================================
-- Calculate growth rates for revenue and profit trends
WITH yearly_performance AS (
    SELECT 
        YEAR(ORDER_DATE) AS fiscal_year,
        ROUND(SUM(SALES), 2) AS annual_revenue,
        ROUND(SUM(PROFIT), 2) AS annual_profit,
        COUNT(DISTINCT ORDER_ID) AS annual_orders,
        COUNT(DISTINCT CUSTOMER_ID) AS annual_customers
    FROM 
        superstore_sales
    WHERE 
        SALES > 0 AND ORDER_DATE IS NOT NULL
    GROUP BY 
        YEAR(ORDER_DATE)
)
SELECT 
    fiscal_year,
    annual_revenue,
    annual_profit,
    annual_orders,
    annual_customers,
    ROUND((annual_revenue - LAG(annual_revenue) OVER (ORDER BY fiscal_year)) / 
          LAG(annual_revenue) OVER (ORDER BY fiscal_year) * 100, 2) AS revenue_growth_pct,
    ROUND((annual_profit - LAG(annual_profit) OVER (ORDER BY fiscal_year)) / 
          LAG(annual_profit) OVER (ORDER BY fiscal_year) * 100, 2) AS profit_growth_pct,
    ROUND((annual_orders - LAG(annual_orders) OVER (ORDER BY fiscal_year)) / 
          LAG(annual_orders) OVER (ORDER BY fiscal_year) * 100, 2) AS order_growth_pct
FROM 
    yearly_performance
ORDER BY 
    fiscal_year ASC;


-- ============================================================================
-- QUERY 11: SHIPPING MODE EFFICIENCY
-- ============================================================================
-- Analyze profit margins by shipping method
SELECT 
    SHIP_MODE,
    COUNT(DISTINCT ORDER_ID) AS orders,
    ROUND(AVG(DATEDIFF(DAY, ORDER_DATE, SHIP_DATE)), 0) AS avg_days_to_ship,
    ROUND(SUM(SALES), 2) AS mode_revenue,
    ROUND(SUM(PROFIT), 2) AS mode_profit,
    ROUND(SUM(PROFIT) / SUM(SALES) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(SALES), 2) AS avg_order_value
FROM 
    superstore_sales
WHERE 
    SALES > 0
GROUP BY 
    SHIP_MODE
ORDER BY 
    mode_profit DESC;


-- ============================================================================
-- QUERY 12: PROFITABILITY DISTRIBUTION (PARETO ANALYSIS)
-- ============================================================================
-- Identify which customers/products drive profit (80/20 rule)
WITH profit_ranked AS (
    SELECT 
        CUSTOMER_ID,
        CUSTOMER_NAME,
        ROUND(SUM(PROFIT), 2) AS customer_profit,
        RANK() OVER (ORDER BY SUM(PROFIT) DESC) AS profit_rank,
        ROUND(SUM(PROFIT) / (SELECT SUM(PROFIT) FROM superstore_sales) * 100, 2) AS profit_contribution_pct
    FROM 
        superstore_sales
    WHERE 
        PROFIT IS NOT NULL
    GROUP BY 
        CUSTOMER_ID, CUSTOMER_NAME
)
SELECT 
    profit_rank,
    CUSTOMER_ID,
    CUSTOMER_NAME,
    customer_profit,
    profit_contribution_pct,
    SUM(profit_contribution_pct) OVER (ORDER BY profit_rank) AS cumulative_profit_pct,
    CASE 
        WHEN SUM(profit_contribution_pct) OVER (ORDER BY profit_rank) <= 20 THEN 'Top 20% Contributors'
        WHEN SUM(profit_contribution_pct) OVER (ORDER BY profit_rank) <= 50 THEN 'Top 50% Contributors'
        WHEN SUM(profit_contribution_pct) OVER (ORDER BY profit_rank) <= 80 THEN 'Top 80% Contributors'
        ELSE 'Remaining Contributors'
    END AS profit_tier
FROM 
    profit_ranked
WHERE 
    profit_rank <= 100
ORDER BY 
    profit_rank ASC;


-- ============================================================================
-- NOTES & BEST PRACTICES
-- ============================================================================
--
-- DATABASE SETUP:
-- Ensure your database contains a table matching this structure:
--
-- CREATE TABLE superstore_sales (
--     ORDER_ID VARCHAR(50) PRIMARY KEY,
--     ORDER_DATE DATE,
--     SHIP_DATE DATE,
--     SHIP_MODE VARCHAR(50),
--     CUSTOMER_ID VARCHAR(50),
--     CUSTOMER_NAME VARCHAR(100),
--     SEGMENT VARCHAR(50),
--     REGION VARCHAR(50),
--     STATE VARCHAR(50),
--     POSTAL_CODE VARCHAR(20),
--     COUNTRY VARCHAR(100),
--     CATEGORY VARCHAR(50),
--     SUB_CATEGORY VARCHAR(50),
--     PRODUCT_ID VARCHAR(50),
--     PRODUCT_NAME VARCHAR(255),
--     SALES DECIMAL(10, 2),
--     QUANTITY INT,
--     DISCOUNT DECIMAL(5, 2),
--     PROFIT DECIMAL(10, 2)
-- );
--
-- QUERY OPTIMIZATION TIPS:
-- 1. Add indexes on frequently filtered columns (ORDER_DATE, REGION, CUSTOMER_ID)
-- 2. Use partitioning by YEAR(ORDER_DATE) for large datasets
-- 3. Consider materialized views for frequently run aggregations
-- 4. Use appropriate date functions for your SQL dialect (SQL Server, PostgreSQL, MySQL)
-- 5. Monitor execution plans and add indexes on JOIN columns
--
-- ============================================================================

