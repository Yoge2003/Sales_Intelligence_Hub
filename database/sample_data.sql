INSERT INTO branches (branch_name, branch_admin_name) VALUES
('Chennai', 'Arun'),
('Bangalore', 'Kiran'),
('Delhi', 'Rahul');

INSERT INTO customer_sales 
(branch_id, date, name, mobile_number, product_name, gross_sales, status)
VALUES
(1, '2026-04-01', 'Ravi', '9876543210', 'DS', 50000, 'Open'),
(2, '2026-04-02', 'Suresh', '9876543211', 'DA', 40000, 'Open'),
(1, '2026-04-03', 'Priya', '9876543212', 'BA', 30000, 'Open'),
(3, '2026-04-04', 'Anita', '9876543213', 'FSD', 60000, 'Open');

INSERT INTO users (username, password, branch_id, role, email) VALUES
('admin1', 'pass123', 1, 'Admin', 'admin1@gmail.com'),
('admin2', 'pass123', 2, 'Admin', 'admin2@gmail.com'),
('superadmin', 'admin123', NULL, 'Super Admin', 'super@gmail.com');

INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES
(1, '2026-04-01', 20000, 'Cash'),
(1, '2026-04-02', 10000, 'UPI'),
(2, '2026-04-02', 15000, 'Card'),
(3, '2026-04-03', 10000, 'Cash');
