// Order Confirmation JavaScript for Grocery Store Application
class OrderConfirmationManager {
    constructor() {
        this.orderData = null;
        this.init();
    }

    async init() {
        await this.loadOrderData();
        this.updateCartCount();
    }

    async loadOrderData() {
        try {
            const urlParams = getUrlParams();
            const orderId = urlParams.order_id;

            if (!orderId) {
                this.showError('Order information not found.');
                return;
            }

            this.orderData = await apiService.getOrder(orderId);
            this.renderConfirmation();
        } catch (error) {
            this.showError('Error loading order information.');
        }
    }

    renderConfirmation() {
        if (!this.orderData) return;
        const confirmationContent = document.getElementById('confirmationContent');

        const orderItemsHTML = this.orderData.order_items.map(item => {
            const product = item.product;
            const priceEach = item.price_per_unit || product.price;
            const lineTotal = item.total_price || (item.quantity * priceEach);
            return `
                <div class="confirm-item">
                    <div class="confirm-item-info">
                        <div class="confirm-item-name">${escapeHtml(product.name)}</div>
                        <div class="confirm-item-qty">Qty: ${item.quantity} × ${formatCurrency(priceEach)}</div>
                    </div>
                    <div class="confirm-item-price">${formatCurrency(lineTotal)}</div>
                </div>
            `;
        }).join('');

        const paymentLabels = {
            credit_card: 'Credit Card', debit_card: 'Debit Card',
            cash_on_delivery: 'Cash on Delivery', digital_wallet: 'Digital Wallet'
        };

        confirmationContent.innerHTML = `
            <div class="confirmation-wrapper">
                <div class="confirmation-icon">✓</div>
                <h1 class="confirmation-title">Order Confirmed!</h1>
                <p class="confirmation-subtitle">
                    Thank you for your order. We'll start processing it right away.
                </p>

                <div class="confirm-card">
                    <h3>Order Details</h3>
                    <div class="confirm-grid">
                        <div><strong>Order Number</strong><br>${escapeHtml(this.orderData.order_number)}</div>
                        <div><strong>Date</strong><br>${formatDate(this.orderData.created_at)}</div>
                        <div><strong>Status</strong><br><span class="status-badge">${this.orderData.status}</span></div>
                        <div><strong>Payment</strong><br>${paymentLabels[this.orderData.payment_method] || this.orderData.payment_method || 'N/A'}</div>
                    </div>
                    ${this.orderData.shipping_address ? `
                        <div style="margin-top:1rem">
                            <strong>Shipping Address</strong><br>
                            <span style="white-space:pre-line">${escapeHtml(this.orderData.shipping_address)}</span>
                        </div>` : ''}
                </div>

                <div class="confirm-card">
                    <h3>Order Items</h3>
                    <div class="confirm-items">${orderItemsHTML}</div>
                    <div class="confirm-total">
                        <span>Total Amount</span>
                        <span>${formatCurrency(this.orderData.total_amount)}</span>
                    </div>
                </div>

                <div class="confirm-card delivery-card">
                    <strong>📦 Estimated Delivery:</strong> ${this.getEstimatedDeliveryDate()}<br>
                    <strong>🚚 Method:</strong> Standard Delivery (Free)
                </div>

                <div class="confirmation-actions">
                    <a href="index.html" class="cta-button">Continue Shopping</a>
                    <button onclick="window.print()" class="add-to-cart-btn" style="width:auto">🖨️ Print</button>
                    <button onclick="orderConfirmationManager.shareOrder()" class="add-to-cart-btn" style="width:auto">📤 Share</button>
                </div>
            </div>
        `;
    }

    showError(message) {
        document.getElementById('confirmationContent').innerHTML = `
            <div style="padding:3rem; text-align:center;">
                <div style="font-size:3rem; margin-bottom:1rem;">⚠️</div>
                <h2 style="color:var(--accent-color); margin-bottom:1rem;">Order Not Found</h2>
                <p style="margin-bottom:2rem;">${message}</p>
                <a href="index.html" class="cta-button">Return to Home</a>
            </div>
        `;
    }

    async shareOrder() {
        const text = `Order #${this.orderData.order_number} - Total: ${formatCurrency(this.orderData.total_amount)} - Grocery Store`;
        await copyToClipboard(text);
    }

    getEstimatedDeliveryDate() {
        const d = new Date();
        d.setDate(d.getDate() + 3);
        return d.toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
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
}

document.addEventListener('DOMContentLoaded', () => {
    window.orderConfirmationManager = new OrderConfirmationManager();
});
