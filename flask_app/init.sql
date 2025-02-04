CREATE DATABASE IF NOT EXISTS flask_app;
USE flask_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

INSERT INTO users (username, password_hash, role) 
VALUES ('Admin', '$2y$10$yWm9qv5/hH68ZJ3SmgdpUuvS/iAE8JB9hHp54QOpVle2NDGc9WJ6m', 'admin')
ON DUPLICATE KEY UPDATE username=username;
