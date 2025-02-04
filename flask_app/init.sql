CREATE DATABASE IF NOT EXISTS flask_app;
USE flask_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

INSERT INTO users (username, password, role) 
VALUES ('Admin', '$2y$12$xG/YV/0aVKM72KzFmsn2RuMeUefGbIY4CRHkK2wJhx0PMOXoUmSqq', 'admin')
ON DUPLICATE KEY UPDATE username=username;

