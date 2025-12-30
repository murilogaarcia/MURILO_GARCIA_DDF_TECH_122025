create database Case_DDF_TECH_dez2025

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-------- "Criando" Tabelas detalhes para a camada gold
CREATE TABLE gold.dim_product AS
SELECT
  p."ProductID"              AS product_id,
  p."Name"                   AS product_name,
  p."ProductNumber"          AS product_number,
  p."Color"                  AS color,
  p."StandardCost"           AS standard_cost,
  p."ListPrice"              AS list_price,
  sc."ProductSubcategoryID"  AS subcategory_id,
  sc."Name"                  AS subcategory_name,
  c."ProductCategoryID"      AS category_id,
  c."Name"                   AS category_name
FROM silver.product p
LEFT JOIN silver.product_subcategory sc
  ON p."ProductSubcategoryID" = sc."ProductSubcategoryID"
LEFT JOIN silver.product_category c
  ON sc."ProductCategoryID" = c."ProductCategoryID";

CREATE TABLE gold.dim_customer AS
SELECT
  cu."CustomerID" AS customer_id,
  cu."PersonID"   AS person_id,
  cu."StoreID"    AS store_id,
  COALESCE(
    NULLIF(TRIM(pe."FirstName" || ' ' || pe."LastName"), ''),
    st."Name",
    'Unknown'
  ) AS customer_name,
  CASE
    WHEN cu."PersonID" IS NOT NULL THEN 'person'
    WHEN cu."StoreID"  IS NOT NULL THEN 'store'
    ELSE 'unknown'
  END AS customer_type
FROM silver.customer cu
LEFT JOIN silver.person pe
  ON cu."PersonID" = pe."BusinessEntityID"
LEFT JOIN silver.store st
  ON cu."StoreID" = st."BusinessEntityID";


CREATE TABLE gold.fact_sales AS
SELECT
  d."SalesOrderID"       AS sales_order_id,
  d."SalesOrderDetailID" AS sales_order_detail_id,
  h."OrderDate"          AS order_date,
  h."CustomerID"         AS customer_id,
  d."ProductID"          AS product_id,
  d."SpecialOfferID"     AS special_offer_id,
  d."OrderQty"           AS order_qty,
  d."UnitPrice"          AS unit_price,
  d."UnitPriceDiscount"  AS unit_price_discount,
  d.gross_revenue,
  d.discount_amount,
  d.net_revenue
FROM silver.sales_order_detail d
JOIN silver.sales_order_header h
  ON d."SalesOrderID" = h."SalesOrderID";


 CREATE TABLE gold.dim_special_offer AS
SELECT
    so."SpecialOfferID"      AS special_offer_id,
    so."Description"         AS description,
    so."Type"                AS offer_type,
    so."Category"            AS category,
    so."DiscountPct"         AS discount_pct,
    so."MinQty"              AS min_qty,
    so."MaxQty"              AS max_qty,
    so."StartDate"::date     AS start_date,
    so."EndDate"::date       AS end_date,
    
    CASE 
        WHEN so."EndDate" < CURRENT_DATE THEN 'Expired'
        WHEN so."StartDate" > CURRENT_DATE THEN 'Scheduled'
        ELSE 'Active'
    END AS offer_status,

    (so."EndDate"::date - so."StartDate"::date) AS duration_days
FROM silver.special_offer so;



CREATE TABLE gold.dim_date AS
SELECT DISTINCT
  order_date::date AS date_day,
  EXTRACT(YEAR  FROM order_date)::int AS year,
  EXTRACT(MONTH FROM order_date)::int AS month,
  TO_CHAR(order_date, 'Mon') AS month_name,
  EXTRACT(DOW   FROM order_date)::int AS day_of_week
FROM gold.fact_sales;


----------------- Criando as views

CREATE OR REPLACE VIEW gold.vw_sales_daily_category AS
SELECT
  f.order_date::date AS date_day,
  p.category_name,
  SUM(f.net_revenue) AS net_revenue,
  SUM(f.order_qty)   AS qty
FROM gold.fact_sales f
JOIN gold.dim_product p
  ON f.product_id = p.product_id
GROUP BY 1,2;


CREATE OR REPLACE VIEW gold.vw_customer_cohort AS
WITH first_purchase AS (
  SELECT customer_id, MIN(order_date::date) AS first_date
  FROM gold.fact_sales
  GROUP BY 1
),
base AS (
  SELECT
    f.customer_id,
    DATE_TRUNC('month', fp.first_date) AS cohort_month,
    DATE_TRUNC('month', f.order_date)  AS order_month,
    SUM(f.net_revenue) AS revenue
  FROM gold.fact_sales f
  JOIN first_purchase fp ON f.customer_id = fp.customer_id
  GROUP BY 1,2,3
)
SELECT
  cohort_month,
  order_month,
  COUNT(DISTINCT customer_id) AS customers,
  SUM(revenue) AS revenue
FROM base
GROUP BY 1,2;

----- Validando numero de linhas 
SELECT COUNT(*) FROM gold.fact_sales;