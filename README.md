# Grocery Store Web Application

A complete, production-ready grocery store web application built with Flask backend and vanilla JavaScript frontend.

## 🛒 Features

- **Product Catalog**: Browse products by category with search and filtering
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout Process**: Complete order placement with shipping information
- **Order Management**: View order history and details
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Updates**: Cart count and product availability
- **Modern UI**: Clean, user-friendly interface with animations

## 🏗️ Tech Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design with Flexbox/Grid
- **Vanilla JavaScript**: No frameworks, pure JavaScript
- **Responsive Design**: Mobile-first approach

### Backend
- **Python 3**: Programming language
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing

### Database
- **MySQL**: Relational database
- **SQL**: Database schema and queries

## 📁 Project Structure

```
Grocery/
├── backend/                    # Flask backend application
│   ├── config/                # Configuration files
│   │   └── config.py         # App configuration
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   └── models.py         # SQLAlchemy models
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   ├── products.py       # Product endpoints
│   │   ├── cart.py           # Cart endpoints
│   │   └── orders.py         # Order endpoints
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py        # Helper functions
│   ├── app.py                 # Main Flask application
│   └── requirements.txt      # Python dependencies
├── frontend/                   # Frontend application
│   ├── css/                   # Stylesheets
│   │   └── style.css         # Main CSS file
│   ├── js/                    # JavaScript files
│   │   ├── api.js            # API service
│   │   ├── utils.js          # Utility functions
│   │   ├── main.js           # Main application logic
│   │   ├── cart.js           # Cart functionality
│   │   ├── checkout.js       # Checkout process
│   │   └── order-confirmation.js # Order confirmation
│   ├── images/                # Product images
│   ├── assets/                # Static assets
│   ├── index.html             # Home page
│   ├── cart.html              # Shopping cart page
│   ├── checkout.html          # Checkout page
│   └── order-confirmation.html # Order confirmation page
├── database/                   # Database files
│   ├── schema.sql             # Database schema
│   └── sample_data.sql        # Sample data
└── README.md                   # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- Node.js (optional, for development tools)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Grocery
```

### 2. Database Setup

#### Install MySQL
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# On macOS (using Homebrew)
brew install mysql

# On Windows
# Download and install from https://dev.mysql.com/downloads/mysql/
```

#### Start MySQL Service
```bash
# On Linux
sudo systemctl start mysql
sudo systemctl enable mysql

# On macOS
brew services start mysql

# On Windows
# Use MySQL Services or start from command line
```

#### Create Database and User
```sql
-- Log in to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE grocery_store;

-- Create user (optional, recommended for production)
CREATE USER 'grocery_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON grocery_store.* TO 'grocery_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

#### Import Schema and Sample Data
```bash
# Import database schema
mysql -u root -p grocery_store < database/schema.sql

# Import sample data
mysql -u root -p grocery_store < database/sample_data.sql
```

### 3. Backend Setup

#### Create Virtual Environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the `backend` directory:
```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=grocery_user
MYSQL_PASSWORD=your_password
MYSQL_DB=grocery_store

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Optional: If using root user
# MYSQL_USER=root
# MYSQL_PASSWORD=your_root_password
```

#### Run the Backend
```bash
# Make sure virtual environment is activated
cd backend

# Run the Flask application
python app.py
```

The backend will be available at `http://localhost:5000`

### 4. Frontend Setup

#### Option 1: Simple File Server (Recommended for development)
```bash
# Navigate to frontend directory
cd frontend

# Start a simple HTTP server
# Python 3
python -m http.server 3000

# Or with Node.js (if installed)
npx serve . -p 3000

# Or with PHP (if installed)
php -S localhost:3000
```

#### Option 2: Live Server Extension (VS Code)
1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html` and select "Open with Live Server"

The frontend will be available at `http://localhost:3000`

## 📱 Access the Application

1. **Frontend**: Open `http://localhost:3000` in your browser
2. **Backend API**: Available at `http://localhost:5000/api`
3. **API Documentation**: Visit `http://localhost:5000` for endpoint information

## 🔧 API Endpoints

### Products
- `GET /api/products` - Get all products (with pagination and filtering)
- `GET /api/products/{id}` - Get specific product
- `GET /api/products/categories` - Get all categories
- `GET /api/products/featured` - Get featured products
- `GET /api/products/category/{id}` - Get products by category

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update/{id}` - Update cart item quantity
- `DELETE /api/cart/remove/{id}` - Remove item from cart
- `DELETE /api/cart/clear` - Clear cart
- `GET /api/cart/count` - Get cart item count

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders` - Get user orders
- `GET /api/orders/{id}` - Get specific order
- `POST /api/orders/{id}/cancel` - Cancel order
- `GET /api/orders/stats` - Get order statistics

### Health Check
- `GET /api/health` - API health check

## 🎯 Example API Requests

### Get Products with Filters
```bash
curl "http://localhost:5000/api/products?page=1&per_page=10&category_id=1&min_price=5&max_price=50"
```

### Add Item to Cart
```bash
curl -X POST "http://localhost:5000/api/cart/add" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Create Order
```bash
curl -X POST "http://localhost:5000/api/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main St, City, State 12345",
    "payment_method": "credit_card",
    "notes": "Please deliver after 5 PM"
  }'
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Run with test configuration
export FLASK_ENV=testing
python app.py
```

### Frontend Testing
Open the application in different browsers and test:
- Responsive design on mobile/tablet/desktop
- Cart functionality
- Checkout process
- Order placement

## 🔒 Security Considerations

### Production Deployment
1. **Environment Variables**: Never commit sensitive data to version control
2. **Database Security**: Use strong passwords and limit database user permissions
3. **HTTPS**: Use SSL/TLS in production
4. **Input Validation**: All inputs are validated on both frontend and backend
5. **SQL Injection**: SQLAlchemy ORM prevents SQL injection
6. **CORS**: Configure CORS properly for production domains

### Recommended Security Headers
```python
# Add to Flask app configuration
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}
```

## 🚀 Deployment

### Backend Deployment (Production)
1. **Web Server**: Use Gunicorn or uWSGI
2. **Reverse Proxy**: Nginx or Apache
3. **Database**: Production MySQL instance
4. **Environment**: Set `FLASK_ENV=production`

Example Gunicorn command:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Deployment
1. **Static Hosting**: Deploy to Netlify, Vercel, or GitHub Pages
2. **CDN**: Use CDN for static assets
3. **HTTPS**: Ensure HTTPS is enabled

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
1. **Database Connection Error**
   - Check MySQL service is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **Module Import Errors**
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **CORS Issues**
   - Check CORS configuration in `config.py`
   - Ensure frontend URL is in allowed origins

#### Frontend Issues
1. **API Connection Errors**
   - Check backend is running on port 5000
   - Verify API base URL in `js/api.js`
   - Check browser console for CORS errors

2. **Styling Issues**
   - Ensure CSS file is properly linked
   - Check browser developer tools for CSS errors

3. **JavaScript Errors**
   - Check browser console for errors
   - Ensure all JavaScript files are loaded

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

## 📈 Performance Optimization

### Backend
1. **Database Indexing**: Proper indexes on frequently queried columns
2. **Connection Pooling**: SQLAlchemy connection pooling
3. **Caching**: Implement Redis caching for frequently accessed data
4. **Pagination**: Limit results per page

### Frontend
1. **Image Optimization**: Compress product images
2. **Lazy Loading**: Implement lazy loading for images
3. **Minification**: Minify CSS and JavaScript in production
4. **CDN**: Use CDN for static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: support@grocerystore.com
- Phone: 1-800-GROCERY
- GitHub Issues: Create an issue in the repository

## 🙏 Acknowledgments

- Flask framework and community
- Bootstrap for design inspiration
- Font Awesome for icons
- All contributors and users of this application
