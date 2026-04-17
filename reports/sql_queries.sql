#All customer sales
SELECT * FROM customer_sales;

#All branches
SELECT * FROM branches;

#All payments
SELECT * FROM payment_splits;

#Open_sales
SELECT * FROM customer_sales
WHERE status = 'Open';

#Chennai branch sales
SELECT * FROM customer_sales
WHERE branch_id = 1;

#Total gross sales
SELECT SUM(gross_sales) AS total_sales
FROM customer_sales;

#Total received amount
SELECT SUM(received_amount) AS total_received
FROM customer_sales;

#Total pending amount
SELECT SUM(pending_amount) AS total_pending
FROM customer_sales;

#Sales count per branch
SELECT branch_id, COUNT(*) AS total_sales
FROM customer_sales
GROUP BY branch_id;

#Average sales
SELECT AVG(gross_sales) AS avg_sales
FROM customer_sales;

#Sales_with_branch_name
SELECT cs.*, b.branch_name
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id;

#Sales_with_total_payment_received
SELECT cs.sale_id, cs.name, SUM(ps.amount_paid) AS total_paid
FROM customer_sales cs
JOIN payment_splits ps ON cs.sale_id = ps.sale_id
GROUP BY cs.sale_id, cs.name;

#Branch-wise total sales
SELECT b.branch_name, SUM(cs.gross_sales) AS total_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
GROUP BY b.branch_name;

#Sales_with payment method
SELECT cs.name, ps.payment_method
FROM customer_sales cs
JOIN payment_splits ps ON cs.sale_id = ps.sale_id;

#Sales_with_admin_name
SELECT cs.name, b.branch_admin_name
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id;

#Pending greated than 5k
SELECT * FROM customer_sales
WHERE pending_amount > 5000;

#Top_3 sales
SELECT * FROM customer_sales
ORDER BY gross_sales DESC
LIMIT 3;

#Best branch
SELECT b.branch_name, SUM(cs.gross_sales) AS total_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
GROUP BY b.branch_name
ORDER BY total_sales DESC
LIMIT 1;

#Monthly sales
SELECT YEAR(date) AS year, MONTH(date) AS month,
SUM(gross_sales) AS total_sales
FROM customer_sales
GROUP BY YEAR(date), MONTH(date);

#Payment method analysis
SELECT payment_method, SUM(amount_paid) AS total
FROM payment_splits
GROUP BY payment_method;