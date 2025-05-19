-- Categories Table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX (name),
    INDEX (category_id)
);

-- Sales Table
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX (sale_date),
    INDEX (product_id)
);

-- Inventory Table (Tracks IN/OUT Changes)
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    stock INT NOT NULL DEFAULT 0,               -- Current stock after this change
    change_type ENUM('IN', 'OUT', 'ADJUSTMENT') NULL, -- Type of inventory change; NULL if this row is just the current state
    quantity INT DEFAULT 0,                      -- Quantity changed in this transaction (0 if this row is current state only)
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reference VARCHAR(255),                      -- Optional reference (sale id, restock order, etc.)
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY (product_id, id),                  -- To ensure rows are unique per change
    INDEX (product_id),
    INDEX (change_date)
);
