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
            
            if (sizeSelect.value === '') {
                e.preventDefault();
                alert('Please select a size');
                return;
            }
            
            if (parseInt(quantityInput.value) > parseInt(quantityInput.getAttribute('max'))) {
                e.preventDefault();
                alert('Quantity exceeds available stock');
                return;
            }
        });
    }
});
