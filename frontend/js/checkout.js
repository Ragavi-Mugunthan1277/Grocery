// Checkout JavaScript for Grocery Store Application
class CheckoutManager {
    constructor() {
        this.cartData = null;
        this.submitting = false;
        this.init();
    }

    async init() {
        await this.loadCartData();
        this.setupEventListeners();
        this.updateCartCount();
    }

    async loadCartData() {
        try {
            const cartResponse = await apiService.getCart();
            if (!cartResponse || !cartResponse.cart_items || cartResponse.cart_items.length === 0) {
                showToast('Your cart is empty. Redirecting...', 'error');
                setTimeout(() => { window.location.href = 'cart.html'; }, 2000);
                return;
            }
            this.cartData = {
                items: cartResponse.cart_items,
                totalAmount: cartResponse.total_amount,
                totalItems: cartResponse.total_items
            };
            this.renderOrderSummary();
        } catch (error) {
            showToast('Error loading cart data', 'error');
        }
    }

    renderOrderSummary() {
        if (!this.cartData) return;
        const summaryContent = document.getElementById('orderSummaryContent');

        const itemsHTML = this.cartData.items.map(item => {
            const product = item.product;
            const itemTotal = item.quantity * product.price;
            return `
                <div class="summary-item">
                    <div class="summary-item-info">
                        <div class="summary-item-name">${escapeHtml(product.name)}</div>
                        <div class="summary-item-qty">Qty: ${item.quantity} × ${formatCurrency(product.price)}</div>
                    </div>
                    <div class="summary-item-price">${formatCurrency(itemTotal)}</div>
                </div>
            `;
        }).join('');

        summaryContent.innerHTML = `
            <div class="summary-items">${itemsHTML}</div>
            <div class="summary-row"><span>Subtotal (${this.cartData.totalItems} items):</span><span>${formatCurrency(this.cartData.totalAmount)}</span></div>
            <div class="summary-row"><span>Delivery:</span><span style="color:var(--primary-color)">FREE</span></div>
            <div class="summary-row total"><span>Total:</span><span>${formatCurrency(this.cartData.totalAmount)}</span></div>
            <div class="delivery-info">
                <strong>📦 Delivery Info</strong><br>
                Free delivery on all orders<br>
                Estimated: 2–3 business days
            </div>
        `;
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;

        if (field.hasAttribute('required') && !value) {
            isValid = false;
        } else if (field.type === 'email' && value && !validateEmail(value)) {
            isValid = false;
        } else if (field.name === 'phone' && value && !validatePhone(value)) {
            isValid = false;
        }

        field.classList.toggle('error', !isValid);
        return isValid;
    }

    async processOrder() {
        if (this.submitting) return;
        const checkoutForm = document.getElementById('checkoutForm');
        const validation = validateForm(checkoutForm);
        if (!validation.isValid) {
            showToast('Please fill in all required fields correctly', 'error');
            return;
        }

        this.submitting = true;
        const submitBtn = checkoutForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            const formData = new FormData(checkoutForm);
            const orderData = {
                shipping_address: `${formData.get('firstName')} ${formData.get('lastName')}\n${formData.get('address')}\nPhone: ${formData.get('phone')}\nEmail: ${formData.get('email')}`,
                payment_method: formData.get('paymentMethod'),
                notes: formData.get('notes') || ''
            };

            const order = await apiService.createOrder(orderData);
            showToast('Order placed successfully!', 'success');
            setTimeout(() => {
                window.location.href = `order-confirmation.html?order_id=${order.order.id}&order_number=${order.order.order_number}`;
            }, 1500);
        } catch (error) {
            showToast(error.message || 'Error processing order. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Place Order';
            this.submitting = false;
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

    setupEventListeners() {
        const checkoutForm = document.getElementById('checkoutForm');
        checkoutForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.processOrder();
        });

        checkoutForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => input.classList.remove('error'));
        });

        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.querySelector('.nav-links');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.checkoutManager = new CheckoutManager();
});
