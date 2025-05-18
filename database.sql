-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS primehomes;
USE primehomes;

-- Create users table with role and password reset fields
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'agent', 'admin') NOT NULL DEFAULT 'user',
    reset_token VARCHAR(255) DEFAULT NULL,
    reset_token_expiry DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert test users (password: Test@123)
INSERT INTO users (email, password, role) VALUES 
('test@example.com', '$2y$10$8tl.1lJ9CpqVXVxzg4awUemf7Xs.XLHvpBQO4HQWUvg0CQ2w5ojIS', 'user'),
('agent@example.com', '$2y$10$8tl.1lJ9CpqVXVxzg4awUemf7Xs.XLHvpBQO4HQWUvg0CQ2w5ojIS', 'agent');

-- Create agent_profiles table
CREATE TABLE IF NOT EXISTS agent_profiles (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    bio TEXT,
    photo_url VARCHAR(255),
    properties_sold INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert test agent profile
INSERT INTO agent_profiles (user_id, full_name, phone, bio) VALUES 
(2, 'John Doe', '+1234567890', 'Experienced real estate agent with over 10 years in the industry.'); 