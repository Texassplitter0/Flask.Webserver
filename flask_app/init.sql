CREATE DATABASE IF NOT EXISTS flask_app;
USE flask_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin', 'editor') DEFAULT 'user'
);

INSERT INTO users (username, password, role) VALUES
('admin', '$2b$12$examplehashedpassword', 'admin');