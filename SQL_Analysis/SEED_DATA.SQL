CREATE DATABASE Mamaearth_Analytics;

USE Mamaearth_Analytics;

CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    city_tier INT NOT NULL,
    signup_date DATE NOT NULL,
    acquisition_source VARCHAR(20) NOT NULL
);

CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    discount_pct INT,
    payment_method VARCHAR(10) NOT NULL,
    rating INT,
    returned INT NOT NULL DEFAULT 0,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

# OVER HERE I HAVE ISERTED TABEL MANUALLY BY import table
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';

select*from customers;   #VERIFY CUSTOMER
SELECT COUNT(*) AS customer_count
FROM customers;

select*from products;              #VERIFY PRODUCT
SELECT COUNT(*) AS product_count
FROM products;

select*from orders;                         #VERIFY ORDER       
SELECT COUNT(*) AS order_count
FROM orders;

SELECT     #FORIEN KEYS ACTUALLY WORKING
    o.order_id,
    o.customer_id,
    c.name,
    o.product_id,
    p.product_name
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id;
    
    # NULL
    SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS non_null_ratings
FROM orders;

SELECT order_id, rating, discount_pct
FROM orders
WHERE rating IS NULL
   OR discount_pct IS NULL;
   
   

