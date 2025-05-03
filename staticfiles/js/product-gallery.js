document.addEventListener('DOMContentLoaded', function() {
    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            navbar.classList.remove('scrolled');
            return;
        }
        
        if (currentScroll > lastScroll && !navbar.classList.contains('scrolled')) {
            navbar.classList.remove('scrolled');
        } else if (currentScroll < lastScroll && navbar.classList.contains('scrolled')) {
            navbar.classList.add('scrolled');
        }
        lastScroll = currentScroll;
    });

    // Product Gallery
    const mainImage = document.querySelector('.main-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const zoomOverlay = document.createElement('div');
    zoomOverlay.className = 'zoom-overlay';
    document.body.appendChild(zoomOverlay);

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const newSrc = this.querySelector('img').src;
            mainImage.querySelector('img').src = newSrc;
            
            // Add active class to clicked thumbnail and remove from others
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Image Zoom on Hover
    mainImage.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.05)';
    });

    mainImage.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });

    // Quantity Counter with Animation
    const quantityInput = document.querySelector('.quantity-input input');
    const plusBtn = document.querySelector('.quantity-btn.plus');
    const minusBtn = document.querySelector('.quantity-btn.minus');

    const updateQuantity = (increment) => {
        const currentValue = parseInt(quantityInput.value);
        const newValue = currentValue + increment;
        
        if (newValue >= parseInt(quantityInput.min) && newValue <= parseInt(quantityInput.max)) {
            quantityInput.value = newValue;
            
            // Animation
            const counter = document.createElement('div');
            counter.className = 'quantity-animation';
            counter.textContent = increment > 0 ? '+' : '-';
            plusBtn.appendChild(counter);
            
            setTimeout(() => {
                counter.remove();
            }, 500);
        }
    };

    plusBtn.addEventListener('click', () => updateQuantity(1));
    minusBtn.addEventListener('click', () => updateQuantity(-1));

    // Color Selector with Animation
    const colorOptions = document.querySelectorAll('.color-option');
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Add active class to clicked color and remove from others
            colorOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            
            // Animation
            const circle = document.createElement('div');
            circle.className = 'color-animation';
            circle.style.backgroundColor = this.style.backgroundColor;
            this.appendChild(circle);
            
            setTimeout(() => {
                circle.remove();
            }, 500);
        });
    });

    // Smooth Scroll for Reviews
    const reviewTabs = document.querySelectorAll('.nav-tabs .nav-link');
    reviewTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize AOS animations
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });

    // Add animations to elements
    const animatedElements = document.querySelectorAll('.product-info, .product-tabs, .reviews-section');
    animatedElements.forEach(element => {
        element.classList.add('aos-init');
        element.setAttribute('data-aos', 'fade-up');
    });

    // Share buttons with Animation
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });

        button.addEventListener('click', function() {
            const url = window.location.href;
            const title = document.querySelector('.product-title').textContent;
            
            // Animation
            const ripple = document.createElement('div');
            ripple.className = 'share-ripple';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 500);

            switch (this.classList[1]) {
                case 'facebook':
                    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}&t=${encodeURIComponent(title)}`, '_blank');
                    break;
                case 'twitter':
                    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`, '_blank');
                    break;
                case 'instagram':
                    window.open(`https://www.instagram.com/create/`, '_blank');
                    break;
                case 'pinterest':
                    window.open(`https://www.pinterest.com/pin/create/button/?url=${encodeURIComponent(url)}&description=${encodeURIComponent(title)}`, '_blank');
                    break;
            }
        });
    });

    // Review Form with Validation and Animation
    const reviewForm = document.querySelector('.review-form form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            const rating = this.querySelector('select[name="rating"]').value;
            const comment = this.querySelector('textarea[name="comment"]').value;
            
            if (!rating || !comment) {
                e.preventDefault();
                
                // Shake animation for invalid form
                this.classList.add('shake');
                setTimeout(() => {
                    this.classList.remove('shake');
                }, 500);
                
                // Show error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.textContent = 'Please fill in both rating and comment before submitting.';
                this.insertBefore(errorMessage, this.firstChild);
                
                setTimeout(() => {
                    errorMessage.remove();
                }, 3000);
            }
        });
    }

    // Related Products Carousel
    const relatedProducts = document.querySelector('.related-products');
    if (relatedProducts) {
        new Swiper(relatedProducts, {
            slidesPerView: 4,
            spaceBetween: 20,
            breakpoints: {
                320: {
                    slidesPerView: 1,
                },
                768: {
                    slidesPerView: 2,
                },
                992: {
                    slidesPerView: 3,
                },
                1200: {
                    slidesPerView: 4,
                },
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            autoplay: {
                delay: 3000,
                disableOnInteraction: false,
            },
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            }
        });
    }

    // Add to Cart Animation
    const addToCartBtn = document.querySelector('.action-buttons .btn-primary');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            // Button animation
            this.style.transform = 'scale(0.95)';
            this.style.opacity = '0.8';
            
            // Create cart animation
            const cartIcon = document.createElement('div');
            cartIcon.className = 'cart-animation';
            document.body.appendChild(cartIcon);
            
            // Show success message
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.textContent = 'Added to cart successfully!';
            document.body.appendChild(successMessage);
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
                this.style.opacity = '1';
                cartIcon.remove();
                successMessage.remove();
            }, 300);
        });
    }
});
