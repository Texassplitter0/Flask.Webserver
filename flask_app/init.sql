CREATE DATABASE IF NOT EXISTS flask_app;
USE flask_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL,
    notes VARCHAR(200) NOT NULL,
    role ENUM('user', 'admin', 'editor') DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS registration_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS game_db (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    score INT NOT NULL
);

INSERT INTO users (username, password, email, notes, role) 
VALUES ('Admin', 'pbkdf2:sha256:1000000$z6xQxoW6plIVe6fV$a009a43c68c63247682d0e493ced3c7d978f2e7dd9c0fbf62b12ce0371e0a019', 'admin@gamedivers.de', 'admin', 'admin')
ON DUPLICATE KEY UPDATE 
    password = VALUES(password),
    email = VALUES(email),
    role = VALUES(role);
