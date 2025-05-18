-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('user', 'agent', 'admin')) NOT NULL DEFAULT 'user',
    reset_token TEXT,
    reset_token_expiry DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create agent_profiles table
CREATE TABLE IF NOT EXISTS agent_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    bio TEXT,
    photo_url TEXT,
    properties_sold INTEGER DEFAULT 0,
    rating REAL DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create properties table
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    type TEXT CHECK(type IN ('rent', 'sell')) NOT NULL,
    status TEXT DEFAULT 'available',
    price REAL NOT NULL,
    address TEXT NOT NULL,
    location TEXT NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    area REAL NOT NULL,
    description TEXT NOT NULL,
    amenities TEXT NOT NULL,
    main_image TEXT NOT NULL,
    gallery_images TEXT,
    property_type TEXT CHECK(property_type IN ('house', 'apartment', 'villa', 'plot')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert test users (password: Test@123)
INSERT INTO users (email, password, role) VALUES 
('test@example.com', '$2y$10$8tl.1lJ9CpqVXVxzg4awUemf7Xs.XLHvpBQO4HQWUvg0CQ2w5ojIS', 'user'),
('agent@example.com', '$2y$10$8tl.1lJ9CpqVXVxzg4awUemf7Xs.XLHvpBQO4HQWUvg0CQ2w5ojIS', 'agent');

-- Insert test agent profile
INSERT INTO agent_profiles (user_id, full_name, phone, bio) VALUES 
(2, 'John Doe', '+1234567890', 'Experienced real estate agent with over 10 years in the industry.'); 