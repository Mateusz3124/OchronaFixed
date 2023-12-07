-- Create the "bank" database
CREATE DATABASE IF NOT EXISTS bank;

-- Use the "bank" database
USE bank;

-- Create a sample table
CREATE TABLE  transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    amount VARCHAR(255),
    account VARCHAR(255),
    name VARCHAR(255),
    surname VARCHAR(255),
    address VARCHAR(255)
);
CREATE TABLE users (
    username VARCHAR(255),
    password VARCHAR(255),
    card VARCHAR(255),
    id VARCHAR(255)
);

