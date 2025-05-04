document.addEventListener('DOMContentLoaded', function() {
    // Quantity buttons
    const minusBtn = document.querySelector('.quantity-btn.minus');
    const plusBtn = document.querySelector('.quantity-btn.plus');
    const quantityInput = document.querySelector('input[name="quantity"]');

    if (minusBtn && plusBtn && quantityInput) {
        minusBtn.addEventListener('click', function() {
            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantityInput.value = quantity - 1;
            }
        });

        plusBtn.addEventListener('click', function() {
            let quantity = parseInt(quantityInput.value);
            const max = parseInt(quantityInput.getAttribute('max'));
            if (quantity < max) {
                quantityInput.value = quantity + 1;
            }
        });
    }

    // Size selection
    const sizeSelect = document.querySelector('select[name="size"]');
    const quantityInput = document.querySelector('input[name="quantity"]');

    if (sizeSelect && quantityInput) {
        sizeSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const stock = parseInt(selectedOption.dataset.stock);
            quantityInput.setAttribute('max', stock);
            
            // Update quantity if it exceeds stock
            if (parseInt(quantityInput.value) > stock) {
                quantityInput.value = stock;
            }
        });
    }

    // Form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!sizeSelect || !quantityInput) return;
            
    const sizeSelect = document.getElementById('sizeSelect');
    const sizeAlert = document.getElementById('sizeAlert');
    const quantityInput = document.getElementById('quantity');
    const decreaseQty = document.getElementById('decreaseQty');
    const increaseQty = document.getElementById('increaseQty');
    const toggleDescriptionBtn = document.getElementById('toggleDescription');
    const descriptionContent = document.querySelector('.product-description .description-content');
    const colorButtons = document.querySelectorAll('.color-btn');
    const form = document.getElementById('productForm');
    const addToCartBtn = document.getElementById('addToCart');
    const minusBtn = document.querySelector('.quantity-btn.minus');
    const plusBtn = document.querySelector('.quantity-btn.plus');

    // Initialize AOS animations
    AOS.init({
        duration: 800,
        once: true
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Quantity Controls
    function updateQuantity(value) {
        const min = 1;
        const max = 100;
        const newValue = Math.max(min, Math.min(max, value));
        quantityInput.value = newValue;
        enableAddToCartButton();
    }

    decreaseQty.addEventListener('click', () => {
        updateQuantity(parseInt(quantityInput.value) - 1);
    });

    increaseQty.addEventListener('click', () => {
        updateQuantity(parseInt(quantityInput.value) + 1);
    });

    minusBtn.addEventListener('click', function() {
        let quantity = parseInt(quantityInput.value);
        if (quantity > 1) {
            quantityInput.value = quantity - 1;
        }
    });

    plusBtn.addEventListener('click', function() {
        let quantity = parseInt(quantityInput.value);
        const max = parseInt(quantityInput.getAttribute('max'));
        if (quantity < max) {
            quantityInput.value = quantity + 1;
        }
    });

    // Size Selection
    sizeSelect.addEventListener('change', function() {
        if (this.value) {
            sizeAlert.style.display = 'none';
            enableAddToCartButton();
        } else {
            sizeAlert.style.display = 'block';
        }
    });

    // Color Selection
    colorButtons.forEach(button => {
        button.addEventListener('click', function() {
            colorButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            enableAddToCartButton();
        });
    });

    // Description Toggle
    let isExpanded = false;
    toggleDescriptionBtn.addEventListener('click', () => {
        isExpanded = !isExpanded;
        descriptionContent.classList.toggle('expanded');
        toggleDescriptionBtn.innerHTML = `<i class="fas fa-chevron-${isExpanded ? 'up' : 'down'}"></i> ${isExpanded ? 'Show less' : 'Show more'}`;
    });

    // Add to Cart Button
    function enableAddToCartButton() {
        const selectedSize = sizeSelect.value;
        const selectedColor = document.querySelector('.color-btn.active');
        
        const hasSize = !!selectedSize;
        const hasColor = !!selectedColor;
        
        addToCartBtn.disabled = !(hasSize && hasColor);
    }

    // Form Handling
    if (form) {
        // Initialize form state
        const selectedSize = sizeSelect.value;
        const quantity = parseInt(quantityInput.value) || 1;

        // Update form values
        sizeSelect.value = selectedSize;
        quantityInput.value = quantity;

        // Enable/disable add to cart button
        enableAddToCartButton();

        // Handle size change
        sizeSelect.addEventListener('change', function() {
            const selectedSize = this.value;
            
            // Update form values
            if (selectedSize) {
                this.value = selectedSize;
            }
            
            // Enable add to cart button
            enableAddToCartButton();
        });

        // Handle color change
        const colorInputs = document.querySelectorAll('.color-btn');
        colorInputs.forEach(input => {
            input.addEventListener('click', function() {
                const selectedSize = sizeSelect.value;
                const selectedColor = this.dataset.color;
                
                // Update form values
                if (selectedSize) {
                    sizeSelect.value = selectedSize;
                }
                
                // Enable add to cart button
                enableAddToCartButton();
            });
        });

        // Handle quantity change
        quantityInput.addEventListener('change', function() {
            const value = parseInt(this.value) || 1;
            this.value = value;
            enableAddToCartButton();
        });

        // Handle form submission
        form.addEventListener('submit', function(e) {
            const selectedSize = sizeSelect.value;
            const selectedColor = document.querySelector('.color-btn.active');
            const quantity = parseInt(quantityInput.value) || 1;
            
            if (!selectedSize || !selectedColor) {
                e.preventDefault();
                alert('Please select both size and color');
                return false;
            }

            // Check stock availability
            const stock = parseInt(selectedSize.dataset.stock);
            if (!selectedSize.value) {
                e.preventDefault();
                alert('Please select a size');
                return false;
            }

            if (quantity > stock) {
                e.preventDefault();
                alert('Quantity exceeds available stock');
                return false;
            }
        });
    }
});
