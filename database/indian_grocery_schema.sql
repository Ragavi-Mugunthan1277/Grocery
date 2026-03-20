-- Indian Grocery Store Database Schema

-- Categories Table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    image_url TEXT
);

-- Products Table
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    image_url TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Insert Categories
INSERT INTO categories (category_name, image_url) VALUES
('Vegetables', 'https://images.unsplash.com/photo-1542838132-92c53300491e'),
('Fruits', 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b'),
('Rice & Grains', 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d'),
('Pulses & Dals', 'https://images.unsplash.com/photo-1586201375761-83865001e31c'),
('Spices', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d'),
('Oils & Ghee', 'https://images.unsplash.com/photo-1627485937980-221c88ac04f4'),
('Dairy Products', 'https://images.unsplash.com/photo-1585238342028-4bbc4b76d3c6');

-- Insert Products - Vegetables
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Onion', 30.00, 1, 'https://source.unsplash.com/400x400/?onion,vegetable'),
('Potato', 25.00, 1, 'https://source.unsplash.com/400x400/?potato,vegetable'),
('Tomato', 28.00, 1, 'https://source.unsplash.com/400x400/?tomato,vegetable');

-- Insert Products - Fruits
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Apple', 150.00, 2, 'https://source.unsplash.com/400x400/?apple,fruit'),
('Banana', 50.00, 2, 'https://source.unsplash.com/400x400/?banana,fruit'),
('Mango', 120.00, 2, 'https://source.unsplash.com/400x400/?mango,fruit');

-- Insert Products - Rice & Grains
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Basmati Rice', 90.00, 3, 'https://source.unsplash.com/400x400/?basmati,rice,grains'),
('Wheat Atta', 55.00, 3, 'https://source.unsplash.com/400x400/?wheat,flour,grains'),
('Rava', 45.00, 3, 'https://source.unsplash.com/400x400/?rava,semolina,grains');

-- Insert Products - Pulses & Dals
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Toor Dal', 140.00, 4, 'https://source.unsplash.com/400x400/?toor,dal,lentils'),
('Moong Dal', 130.00, 4, 'https://source.unsplash.com/400x400/?moong,dal,lentils'),
('Chana Dal', 110.00, 4, 'https://source.unsplash.com/400x400/?chana,dal,lentils');

-- Insert Products - Spices
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Turmeric Powder', 40.00, 5, 'https://source.unsplash.com/400x400/?turmeric,spice'),
('Red Chilli Powder', 60.00, 5, 'https://source.unsplash.com/400x400/?chilli,powder,spice'),
('Garam Masala', 80.00, 5, 'https://source.unsplash.com/400x400/?garam,masala,spice');

-- Insert Products - Oils & Ghee
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Mustard Oil', 120.00, 6, 'https://source.unsplash.com/400x400/?mustard,oil,cooking'),
('Refined Sunflower Oil', 110.00, 6, 'https://source.unsplash.com/400x400/?sunflower,oil,cooking'),
('Pure Ghee', 280.00, 6, 'https://source.unsplash.com/400x400/?ghee,cooking');

-- Insert Products - Dairy Products
INSERT INTO products (product_name, price, category_id, image_url) VALUES
('Milk', 28.00, 7, 'https://source.unsplash.com/400x400/?milk,dairy'),
('Curd', 35.00, 7, 'https://source.unsplash.com/400x400/?curd,dairy'),
('Paneer', 90.00, 7, 'https://source.unsplash.com/400x400/?paneer,dairy');
