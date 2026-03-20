// Main JavaScript for Grocery Store Application
class GroceryStore {
    constructor() {
        this.categories = [];
        this.currentFilters = {};
        this.currentPage = 1;
        this.init();
    }

    async init() {
        await this.loadInitialData();
        this.setupEventListeners();
        this.updateCartCount();
    }

    async loadInitialData() {
        try {
            await this.loadCategories();
            await this.loadFeaturedProducts();
            await this.loadProducts();
        } catch (error) {
            showToast('Error loading products. Please try again.', 'error');
        }
    }

    async loadCategories() {
        try {
            this.categories = await apiService.getCategories();
            this.renderCategories();
            this.populateCategoryFilter();
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    renderCategories() {
        const categoryGrid = document.getElementById('categoryGrid');
        const categoryIcons = {
            'Vegetables': '🥬', 'Fruits': '🍎', 'Dairy': '🥛',
            'Rice & Grains': '🌾', 'Pulses & Dals': '🫘',
            'Spices': '🌶️', 'Oils & Ghee': '🫒', 'Dairy Products': '🥛'
        };
        categoryGrid.innerHTML = this.categories.map(category => `
            <div class="category-card" onclick="groceryStore.filterByCategory(${category.id})">
                <div class="category-icon">${categoryIcons[category.name] || '📦'}</div>
                <div class="category-name">${escapeHtml(category.name)}</div>
            </div>
        `).join('');
    }

    populateCategoryFilter() {
        const categoryFilter = document.getElementById('categoryFilter');
        const options = this.categories.map(c =>
            `<option value="${c.id}">${escapeHtml(c.name)}</option>`
        ).join('');
        categoryFilter.innerHTML = '<option value="">All Categories</option>' + options;
    }

    async loadFeaturedProducts() {
        try {
            const products = await apiService.getFeaturedProducts(8);
            const grid = document.getElementById('featuredProductsGrid');
            if (products && products.length > 0) {
                grid.innerHTML = products.map(p => this.renderProductCard(p)).join('');
            } else {
                grid.innerHTML = '<p class="no-results">No featured products available.</p>';
            }
        } catch (error) {
            document.getElementById('featuredProductsGrid').innerHTML =
                '<p class="no-results">Could not load featured products.</p>';
        }
    }

    async loadProducts(page = 1, filters = {}) {
        try {
            showLoading('#productsGrid');
            const params = { page, per_page: 12, ...filters };
            const response = await apiService.getProducts(params);
            this.currentPage = page;
            this.currentFilters = filters;
            this.renderProducts(response.products);
            this.renderPagination(response.pagination);
        } catch (error) {
            document.getElementById('productsGrid').innerHTML =
                '<p class="no-results">Error loading products. Please try again.</p>';
        }
    }

    renderProducts(products) {
        const grid = document.getElementById('productsGrid');
        if (!products || products.length === 0) {
            grid.innerHTML = '<p class="no-results">No products found matching your criteria.</p>';
            return;
        }
        grid.innerHTML = products.map(p => this.renderProductCard(p)).join('');
    }

    renderProductCard(product) {
        const imageUrl = `http://localhost:5000/api/product-image/${product.id}`;
        const isInStock = product.stock_quantity > 0;
        return `
            <div class="product-card">
                <img class="product-image" src="${imageUrl}" alt="${escapeHtml(product.name)}"
                     loading="lazy" onerror="this.src='https://placehold.co/400x250/e8f5e9/2ecc71?text=${encodeURIComponent(product.name)}'">
                <div class="product-info">
                    <h3 class="product-name">${escapeHtml(product.name)}</h3>
                    <p class="product-description">${escapeHtml(truncateText(product.description || '', 80))}</p>
                    <div class="product-price">${formatCurrency(product.price)}</div>
                    <button class="add-to-cart-btn" onclick="groceryStore.addToCart(${product.id})"
                            ${!isInStock ? 'disabled' : ''}>
                        ${isInStock ? '🛒 Add to Cart' : 'Out of Stock'}
                    </button>
                </div>
            </div>
        `;
    }

    renderPagination(pagination) {
        const paginationDiv = document.getElementById('pagination');
        if (!pagination || pagination.pages <= 1) {
            paginationDiv.innerHTML = '';
            return;
        }
        let html = '';
        if (pagination.page > 1) {
            html += `<button class="page-btn" onclick="groceryStore.loadProducts(${pagination.page - 1}, groceryStore.currentFilters)">‹ Prev</button>`;
        }
        for (let i = 1; i <= pagination.pages; i++) {
            html += `<button class="page-btn ${i === pagination.page ? 'active' : ''}"
                onclick="groceryStore.loadProducts(${i}, groceryStore.currentFilters)">${i}</button>`;
        }
        if (pagination.page < pagination.pages) {
            html += `<button class="page-btn" onclick="groceryStore.loadProducts(${pagination.page + 1}, groceryStore.currentFilters)">Next ›</button>`;
        }
        paginationDiv.innerHTML = html;
    }

    async addToCart(productId) {
        try {
            await apiService.addToCart(productId, 1);
            showToast('Added to cart!', 'success');
            this.updateCartCount();
        } catch (error) {
            showToast('Error adding to cart. Please try again.', 'error');
        }
    }

    async updateCartCount() {
        try {
            const response = await apiService.getCartCount();
            const cartCount = document.getElementById('cartCount');
            if (cartCount) {
                cartCount.textContent = response.total_items;
                cartCount.style.display = response.total_items > 0 ? 'flex' : 'none';
            }
        } catch (error) { /* silently fail */ }
    }

    filterByCategory(categoryId) {
        document.getElementById('categoryFilter').value = categoryId;
        this.searchProducts();
        document.getElementById('products').scrollIntoView({ behavior: 'smooth' });
    }

    searchProducts() {
        const search = document.getElementById('searchInput').value.trim();
        const categoryId = document.getElementById('categoryFilter').value;
        const minPrice = document.getElementById('minPrice').value;
        const maxPrice = document.getElementById('maxPrice').value;
        const filters = {};
        if (search) filters.search = search;
        if (categoryId) filters.category_id = categoryId;
        if (minPrice) filters.min_price = parseFloat(minPrice);
        if (maxPrice) filters.max_price = parseFloat(maxPrice);
        this.loadProducts(1, filters);
    }

    resetFilters() {
        document.getElementById('searchInput').value = '';
        document.getElementById('categoryFilter').value = '';
        document.getElementById('minPrice').value = '';
        document.getElementById('maxPrice').value = '';
        this.loadProducts(1, {});
    }

    setupEventListeners() {
        document.getElementById('searchBtn').addEventListener('click', () => this.searchProducts());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetFilters());
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchProducts();
        });
        document.getElementById('searchInput').addEventListener('input', debounce(() => this.searchProducts(), 400));

        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.querySelector('.nav-links');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
        }

        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.groceryStore = new GroceryStore();
});
