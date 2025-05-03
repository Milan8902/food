document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add cart count update
    function updateCartCount() {
        const cartItems = document.querySelectorAll('.cart-item');
        const count = cartItems.length;
        document.getElementById('cart-count').textContent = count;
    }

    // Update cart count when page loads
    updateCartCount();

    // Update cart count when items are added/removed
    document.querySelectorAll('form[action*="add_to_cart"]').forEach(form => {
        form.addEventListener('submit', function() {
            setTimeout(updateCartCount, 1000);
        });
    });

    // Add animation to cards when they appear
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });

    // Add quantity change handler for cart items
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
});

// Add to cart button handler
function addToCart(shoeId) {
    const form = document.getElementById(`add-to-cart-form-${shoeId}`);
    if (form) {
        form.submit();
    }
}
