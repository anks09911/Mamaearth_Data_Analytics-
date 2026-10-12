USE Mamaearth_Analytics;

#ORDER TOTAL
select
    COUNT(*) AS total_orders,
    CAST(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        )
        AS DECIMAL(10,2)
    ) AS total_revenue,
    CAST(
        AVG(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        )
        AS DECIMAL(10,2)
    ) AS avg_order_value
FROM orders o
JOIN products p
    ON o.product_id = p.product_id;
    
    #COUNT(*) VS COUNT(COL)
    SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS rated_orders,
    COUNT(*) - COUNT(rating) AS unrated_orders
FROM orders;

#LET JOIN + NOTIN
SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
HAVING COUNT(o.order_id) = 0;

SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN
(
    SELECT DISTINCT customer_id
    FROM orders
);

#GROUP BY + HAVING
SELECT
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.returned) AS returned_orders,
    CAST(
        ROUND(
            100.0 * SUM(o.returned) / COUNT(o.order_id),
            1
        )
        AS DECIMAL(5,1)
    ) AS return_rate_pct
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.city
HAVING
    100.0 * SUM(o.returned) / COUNT(o.order_id) > 20
ORDER BY return_rate_pct DESC;

#ORDER BY +LIMIT/OFFSET
SELECT
    c.customer_id,
    c.name,
    CAST(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ) AS DECIMAL(10,2)
    ) AS total_spend
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC
LIMIT 3 OFFSET 2;

# three table join
SELECT
    p.category,
    COUNT(o.order_id) AS order_count,
    CAST(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        )
        AS DECIMAL(10,2)
    ) AS category_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;

#like
SELECT
    customer_id,
    name
FROM customers
WHERE name LIKE 'A%'
ORDER BY customer_id;

#distinct
SELECT DISTINCT
    acquisition_source
FROM customers
ORDER BY acquisition_source;

# alter + update case
ALTER TABLE customers
ADD loyalty_tier VARCHAR(10);

UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END;
    SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier
ORDER BY loyalty_tier;