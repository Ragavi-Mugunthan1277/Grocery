// Cart JavaScript for Grocery Store Application
class CartManager {
    constructor() {
        this.cartItems = [];
        this.totalAmount = 0;
        this.totalItems = 0;
        this.init();
    }

    async init() {
        await this.loadCart();
        this.setupEventListeners();
        this.updateCartCount();
    }

    async loadCart() {
        try {
            const response = await apiService.getCart();
            this.cartItems = response.cart_items;
            this.totalAmount = response.total_amount;
            this.totalItems = response.total_items;
            this.renderCart();
        } catch (error) {
            console.error('Error loading cart:', error);
            this.renderEmptyCart();
        }
    }

    renderCart() {
        const cartContent = document.getElementById('cartContent');
        if (this.cartItems.length === 0) {
            this.renderEmptyCart();
            return;
        }
        cartContent.innerHTML = `
            <div class="cart-items">
                ${this.cartItems.map(item => this.renderCartItem(item)).join('')}
            </div>
            <div class="cart-summary">
                <div class="summary-row">
                    <span>Subtotal (${this.totalItems} items):</span>
                    <span>${formatCurrency(this.totalAmount)}</span>
                </div>
                <div class="summary-row">
                    <span>Delivery:</span>
                    <span style="color: var(--primary-color);">FREE</span>
                </div>
                <div class="summary-row total">
                    <span>Total:</span>
                    <span>${formatCurrency(this.totalAmount)}</span>
                </div>
                <button class="checkout-btn" onclick="cartManager.proceedToCheckout()">
                    Proceed to Checkout →
                </button>
                <button class="add-to-cart-btn" style="background-color: var(--text-light); margin-top: 0.5rem;"
                        onclick="window.location.href='index.html'">
                    ← Continue Shopping
                </button>
                <button class="remove-btn" style="width:100%; margin-top: 0.5rem;"
                        onclick="cartManager.clearCart()">
                    Clear Cart
                </button>
            </div>
        `;
    }

    renderEmptyCart() {
        document.getElementById('cartContent').innerHTML = `
            <div class="cart-empty">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🛒</div>
                <h2>Your cart is empty</h2>
                <p>Looks like you haven't added any products yet.</p>
                <a href="index.html" class="cta-button" style="display: inline-block; margin-top: 1.5rem;">
                    Start Shopping
                </a>
            </div>
        `;
    }

    renderCartItem(item) {
        const product = item.product;
        const imageUrl = `http://localhost:5000/api/product-image/${product.id}`;
        const itemTotal = item.quantity * product.price;
        return `
            <div class="cart-item" data-item-id="${item.id}">
                <div class="cart-item-image">
                    <img src="${imageUrl}" alt="${escapeHtml(product.name)}"
                         onerror="this.src='https://placehold.co/100x100/e8f5e9/2ecc71?text=${encodeURIComponent(product.name)}'">
                </div>
                <div class="cart-item-details">
                    <h3 class="cart-item-name">${escapeHtml(product.name)}</h3>
                    <p class="cart-item-price">${formatCurrency(product.price)} each</p>
                </div>
                <div class="cart-item-quantity">
                    <button class="quantity-btn" onclick="cartManager.updateQuantity(${item.id}, ${item.quantity - 1})">−</button>
                    <input type="number" class="quantity-input" value="${item.quantity}" min="1"
                           onchange="cartManager.updateQuantity(${item.id}, parseInt(this.value) || 1)">
                    <button class="quantity-btn" onclick="cartManager.updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
                <div class="cart-item-total">
                    <div class="cart-item-total-price">${formatCurrency(itemTotal)}</div>
                    <button class="remove-btn" onclick="cartManager.removeFromCart(${item.id})">Remove</button>
                </div>
            </div>
        `;
    }

    async updateQuantity(itemId, newQuantity) {
        if (newQuantity < 1) {
            await this.removeFromCart(itemId);
            return;
        }
        try {
            await apiService.updateCartItem(itemId, newQuantity);
            await this.loadCart();
            this.updateCartCount();
        } catch (error) {
            showToast('Error updating quantity', 'error');
        }
    }

    async removeFromCart(itemId) {
        if (!confirm('Remove this item from your cart?')) return;
        try {
            await apiService.removeFromCart(itemId);
            showToast('Item removed', 'success');
            await this.loadCart();
            this.updateCartCount();
        } catch (error) {
            showToast('Error removing item', 'error');
        }
    }

    async clearCart() {
        if (!confirm('Clear your entire cart?')) return;
        try {
            await apiService.clearCart();
            showToast('Cart cleared', 'success');
            await this.loadCart();
            this.updateCartCount();
        } catch (error) {
            showToast('Error clearing cart', 'error');
        }
    }

    proceedToCheckout() {
        window.location.href = 'checkout.html';
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

    setupEventListeners() {
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.querySelector('.nav-links');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.cartManager = new CartManager();
});
