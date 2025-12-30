| table       | check      | column         | value    |   pct_failed |
|:------------|:-----------|:---------------|:---------|-------------:|
| customer    | total_rows |                | 19820    |            0 |
| fact_sales  | not_null   | customer_id    |          |            0 |
| fact_sales  | not_null   | order_date     |          |            0 |
| fact_sales  | not_null   | product_id     |          |            0 |
| fact_sales  | not_null   | sales_order_id |          |            0 |
| fact_sales  | range      | gross_revenue  | [0,None] |            0 |
| fact_sales  | range      | net_revenue    | [0,None] |            0 |
| fact_sales  | range      | order_qty      | [0,None] |            0 |
| fact_sales  | range      | unit_price     | [0,None] |            0 |
| fact_sales  | total_rows |                | 121317   |            0 |
| product     | total_rows |                | 504      |            0 |
| sales_offer | total_rows |                | 16       |            0 |
