CREATE TABLE IF NOT EXISTS products (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    product_name TEXT NOT NULL,

    category TEXT,

    brand TEXT,

    buying_price REAL,

    selling_price REAL,

    quantity INTEGER DEFAULT 0,

    minimum_stock INTEGER DEFAULT 5,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fullname TEXT NOT NULL,

    phone TEXT,

    email TEXT,

    age INTEGER,

    gender TEXT,

    role TEXT DEFAULT 'Owner',

    password TEXT,

    profile_image TEXT DEFAULT 'profile.jpg',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    fullname TEXT,

    role TEXT DEFAULT 'Owner'

);



INSERT INTO users
(username,password,fullname,role)

VALUES

('admin','12345','Juma Mussa','Owner');