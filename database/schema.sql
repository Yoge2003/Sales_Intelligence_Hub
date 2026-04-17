CREATE DATABASE guvi_sms;
USE guvi_sms;

CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_admin_name VARCHAR(100) NOT NULL
);

CREATE TABLE customer_sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_id INT,
    date DATE,
    name VARCHAR(100),
    mobile_number VARCHAR(15) UNIQUE,
    product_name VARCHAR(30),
    gross_sales DECIMAL(12,2),
    received_amount DECIMAL(12,2) DEFAULT 0,
    pending_amount DECIMAL(12,2) GENERATED ALWAYS AS (gross_sales - received_amount) STORED,
    status ENUM('Open','Close'),

    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255),
    branch_id INT,
    role ENUM('Super Admin', 'Admin'),
    email VARCHAR(255) UNIQUE,

    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE payment_splits (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT,
    payment_date DATE,
    amount_paid DECIMAL(12,2),
    payment_method VARCHAR(50),

    FOREIGN KEY (sale_id) REFERENCES customer_sales(sale_id)
);



