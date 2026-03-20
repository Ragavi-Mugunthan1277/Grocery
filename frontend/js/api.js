// API Service for Grocery Store Application
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : 'https://YOUR_BACKEND_URL/api'; // Replace with your deployed backend URL

class ApiService {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.sessionId = this.getOrCreateSessionId();
    }

    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('grocery_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('grocery_session_id', sessionId);
        }
        return sessionId;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': this.sessionId,
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async get(endpoint) { return this.request(endpoint, { method: 'GET' }); }
    async post(endpoint, data) {
        return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) });
    }
    async put(endpoint, data) {
        return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data) });
    }
    async delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }

    // Products
    async getProducts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.get(queryString ? `/products?${queryString}` : '/products');
    }
    async getProduct(productId) { return this.get(`/products/${productId}`); }
    async getCategories() { return this.get('/products/categories'); }
    async getFeaturedProducts(limit = 8) { return this.get(`/products/featured?limit=${limit}`); }

    // Cart
    async getCart() { return this.get('/cart'); }
    async addToCart(productId, quantity = 1) {
        return this.post('/cart/add', { product_id: productId, quantity });
    }
    async updateCartItem(itemId, quantity) {
        return this.put(`/cart/update/${itemId}`, { quantity });
    }
    async removeFromCart(itemId) { return this.delete(`/cart/remove/${itemId}`); }
    async clearCart() { return this.delete('/cart/clear'); }
    async getCartCount() { return this.get('/cart/count'); }

    // Orders
    async createOrder(orderData) { return this.post('/orders', orderData); }
    async getOrder(orderId) { return this.get(`/orders/${orderId}`); }

    // Health
    async healthCheck() { return this.get('/health'); }
}

const apiService = new ApiService();
window.apiService = apiService;
