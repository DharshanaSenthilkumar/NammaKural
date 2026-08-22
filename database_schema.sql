CREATE DATABASE IF NOT EXISTS nammakkural;

USE nammakkural;

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(20),
    item VARCHAR(100),
    quantity FLOAT,
    unit VARCHAR(20),
    amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);