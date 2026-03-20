-- Sample Data for Grocery Store Database
USE grocery_store;

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Fruits & Vegetables', 'Fresh fruits and vegetables'),
('Dairy & Eggs', 'Milk, cheese, yogurt, and eggs'),
('Bakery', 'Bread, pastries, and baked goods'),
('Meat & Fish', 'Fresh meat, poultry, and seafood'),
('Pantry Staples', 'Rice, pasta, flour, and cooking essentials'),
('Beverages', 'Juices, soft drinks, and water'),
('Snacks', 'Chips, cookies, and confectionery'),
('Frozen Foods', 'Frozen meals, vegetables, and desserts');

-- Insert sample products
INSERT INTO products (name, description, price, category_id, stock_quantity, image_url) VALUES
-- Fruits & Vegetables
('Fresh Apples', 'Crisp and sweet red apples', 3.99, 1, 100, 'images/apples.jpg'),
('Bananas', 'Ripe yellow bananas', 2.49, 1, 150, 'images/bananas.jpg'),
('Tomatoes', 'Fresh red tomatoes', 4.99, 1, 80, 'images/tomatoes.jpg'),
('Lettuce', 'Crisp green lettuce', 2.99, 1, 60, 'images/lettuce.jpg'),
('Carrots', 'Fresh orange carrots', 3.49, 1, 90, 'images/carrots.jpg'),

-- Dairy & Eggs
('Whole Milk', 'Fresh whole milk 1 gallon', 4.99, 2, 50, 'images/milk.jpg'),
('Greek Yogurt', 'Plain Greek yogurt 32oz', 5.99, 2, 40, 'images/yogurt.jpg'),
('Cheddar Cheese', 'Sharp cheddar cheese block', 6.99, 2, 30, 'images/cheese.jpg'),
('Large Eggs', 'Dozen large eggs', 3.99, 2, 60, 'images/eggs.jpg'),
('Butter', 'Salted butter 1lb', 4.49, 2, 45, 'images/butter.jpg'),

-- Bakery
('Whole Wheat Bread', 'Fresh whole wheat bread', 3.49, 3, 40, 'images/bread.jpg'),
('Croissants', 'Buttery croissants pack of 6', 5.99, 3, 25, 'images/croissants.jpg'),
('Bagels', 'Fresh bagels pack of 6', 4.99, 3, 30, 'images/bagels.jpg'),
('Chocolate Cake', 'Delicious chocolate cake', 12.99, 3, 15, 'images/cake.jpg'),
('Cookies', 'Chocolate chip cookies pack', 4.99, 3, 35, 'images/cookies.jpg'),

-- Meat & Fish
('Chicken Breast', 'Boneless chicken breast 1lb', 8.99, 4, 40, 'images/chicken.jpg'),
('Ground Beef', 'Lean ground beef 1lb', 7.99, 4, 35, 'images/beef.jpg'),
('Salmon Fillet', 'Fresh salmon fillet 1lb', 12.99, 4, 20, 'images/salmon.jpg'),
('Pork Chops', 'Fresh pork chops 1lb', 9.99, 4, 25, 'images/pork.jpg'),
('Shrimp', 'Frozen shrimp 1lb', 10.99, 4, 30, 'images/shrimp.jpg'),

-- Pantry Staples
('White Rice', 'Long grain white rice 5lb', 6.99, 5, 50, 'images/rice.jpg'),
('Pasta', 'Italian pasta 1lb', 2.99, 5, 80, 'images/pasta.jpg'),
('Olive Oil', 'Extra virgin olive oil 500ml', 8.99, 5, 40, 'images/oil.jpg'),
('All-Purpose Flour', 'All-purpose flour 5lb', 4.99, 5, 45, 'images/flour.jpg'),
('Sugar', 'White granulated sugar 4lb', 3.99, 5, 55, 'images/sugar.jpg'),

-- Beverages
('Orange Juice', 'Fresh orange juice 64oz', 4.99, 6, 40, 'images/juice.jpg'),
('Mineral Water', 'Spring water case of 24', 5.99, 6, 60, 'images/water.jpg'),
('Cola', 'Classic cola 12-pack', 6.99, 6, 50, 'images/cola.jpg'),
('Green Tea', 'Green tea bags pack of 20', 3.99, 6, 45, 'images/tea.jpg'),
('Coffee', 'Ground coffee 12oz', 7.99, 6, 35, 'images/coffee.jpg'),

-- Snacks
('Potato Chips', 'Classic potato chips', 3.99, 7, 60, 'images/chips.jpg'),
('Chocolate Bar', 'Milk chocolate bar', 2.99, 7, 80, 'images/chocolate.jpg'),
('Popcorn', 'Microwave popcorn pack', 4.99, 7, 50, 'images/popcorn.jpg'),
('Nuts', 'Mixed nuts 12oz', 6.99, 7, 40, 'images/nuts.jpg'),
('Crackers', 'Whole wheat crackers', 3.49, 7, 55, 'images/crackers.jpg'),

-- Frozen Foods
('Frozen Pizza', 'Pepperoni pizza', 7.99, 8, 30, 'images/pizza.jpg'),
('Ice Cream', 'Vanilla ice cream 1.5qt', 5.99, 8, 40, 'images/icecream.jpg'),
('Frozen Vegetables', 'Mixed vegetables 16oz', 2.99, 8, 60, 'images/frozen_veg.jpg'),
('Frozen Dinner', 'Beef lasagna', 6.99, 8, 35, 'images/dinner.jpg'),
('Waffles', 'Frozen waffles pack', 4.99, 8, 45, 'images/waffles.jpg');

-- Insert sample users
INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address) VALUES
('john_doe', 'john@example.com', 'hashed_password_1', 'John', 'Doe', '555-0101', '123 Main St, City, State 12345'),
('jane_smith', 'jane@example.com', 'hashed_password_2', 'Jane', 'Smith', '555-0102', '456 Oak Ave, City, State 12345'),
('bob_wilson', 'bob@example.com', 'hashed_password_3', 'Bob', 'Wilson', '555-0103', '789 Pine Rd, City, State 12345');
