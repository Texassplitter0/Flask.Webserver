CREATE DATABASE IF NOT EXISTS flask_app;
USE flask_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin', 'editor') DEFAULT 'user'
);

INSERT INTO users (username, password, role) 
VALUES ('Admin', '1$k3gK4qOs7RDbysv2$9234360b86c9da0495c3dc04ee95002ab6462ed2b0662c8f7d85e1ef85e09ef776b1663585886628443fa76201b36fa41aa8fdbb8fbddc5c54a2cc6a5a8e004b', 'admin')
ON DUPLICATE KEY UPDATE username=username;

