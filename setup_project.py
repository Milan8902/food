import os
import subprocess
from pathlib import Path

def create_directories():
    base_dir = Path('shoe_shop')
    
    # Create main directories
    os.makedirs(base_dir / 'static' / 'css', exist_ok=True)
    os.makedirs(base_dir / 'static' / 'js', exist_ok=True)
    os.makedirs(base_dir / 'static' / 'images', exist_ok=True)
    os.makedirs(base_dir / 'templates', exist_ok=True)
    os.makedirs(base_dir / 'media', exist_ok=True)
    os.makedirs(base_dir / 'shoes', exist_ok=True)
    
    # Create Django project structure
    subprocess.run(['django-admin', 'startproject', 'shoe_shop', str(base_dir)])
    subprocess.run(['python', str(base_dir / 'manage.py'), 'startapp', 'shoes'], cwd=str(base_dir))

def create_files():
    base_dir = Path('shoe_shop')
    
    # Create models.py
    with open(base_dir / 'shoes' / 'models.py', 'w') as f:
        f.write("""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
    super().save(*args, **kwargs)

def __str__(self):
    return self.name

class Shoe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shoe_images/')
    stock = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
    super().save(*args, **kwargs)

def __str__(self):
    return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.quantity} x {self.shoe.name} in cart {self.cart.id}"
""")

    # Create admin.py
    with open(base_dir / 'shoes' / 'admin.py', 'w') as f:
        f.write("""
from django.contrib import admin
from .models import Category, Shoe, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'shoe', 'quantity', 'added_at')
    list_filter = ('added_at',)
""")

    # Create views.py
    with open(base_dir / 'shoes' / 'views.py', 'w') as f:
        f.write("""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shoe, Category, Cart, CartItem
from .forms import CartForm

def home(request):
    categories = Category.objects.all()
    featured_shoes = Shoe.objects.filter(is_featured=True)[:6]
    return render(request, 'home.html', {
        'categories': categories,
        'featured_shoes': featured_shoes
    })

def shop(request):
    categories = Category.objects.all()
    shoes = Shoe.objects.all()
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        shoes = shoes.filter(category__slug=category_slug)
    
    return render(request, 'shop.html', {
        'categories': categories,
        'shoes': shoes
    })

def product_detail(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    return render(request, 'product_detail.html', {'shoe': shoe})

@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@login_required
def add_to_cart(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    form = CartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        if quantity <= shoe.stock:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, shoe=shoe)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Added {quantity} {shoe.name}(s) to cart')
        else:
            messages.error(request, f'Only {shoe.stock} {shoe.name}(s) available')
    
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart')
""")

    # Create forms.py
    with open(base_dir / 'shoes' / 'forms.py', 'w') as f:
        f.write("""
from django import forms
from .models import Shoe

class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = ['name', 'description', 'price', 'category', 'image', 'stock', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
""")

    # Create urls.py for shoes app
    with open(base_dir / 'shoes' / 'urls.py', 'w') as f:
        f.write("""
from django.urls import path
from . import views

app_name = 'shoes'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:shoe_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
""")

    # Create main urls.py
    with open(base_dir / 'shoe_shop' / 'urls.py', 'w') as f:
        f.write("""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shoes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""")

    # Create templates
    template_dir = base_dir / 'templates'
    
    # Create base.html
    with open(template_dir / 'base.html', 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shoe Shop</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Shoe Shop</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'shop' %}">Shop</a>
                    </li>
                    {% if user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'cart' %}">Cart</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Login</a>
                    </li>
                    {% endif %}
                </ul>
                {% if user.is_authenticated %}
                <span class="navbar-text text-light">
                    Welcome, {{ user.username }}
                </span>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <footer class="bg-dark text-light mt-5 py-3">
        <div class="container text-center">
            <p>&copy; 2025 Shoe Shop. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
""")

    # Create shop.html
    with open(template_dir / 'shop.html', 'w') as f:
        f.write("""
{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-3">
        <h4>Categories</h4>
        <div class="list-group">
            <a href="{% url 'shop' %}" class="list-group-item list-group-item-action {% if not request.GET.category %}active{% endif %}">
                All Shoes
            </a>
            {% for category in categories %}
            <a href="{% url 'shop' %}?category={{ category.slug }}" class="list-group-item list-group-item-action {% if request.GET.category == category.slug %}active{% endif %}">
                {{ category.name }}
            </a>
            {% endfor %}
        </div>
    </div>

    <div class="col-md-9">
        <h4>Shoes</h4>
        <div class="row">
            {% for shoe in shoes %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="{{ shoe.image.url }}" class="card-img-top" alt="{{ shoe.name }}">
                    <div class="card-body">
                        <h5 class="card-title">{{ shoe.name }}</h5>
                        <p class="card-text">{{ shoe.description|truncatewords:10 }}</p>
                        <p class="card-text"><strong>${{ shoe.price }}</strong></p>
                        <div class="d-flex justify-content-between align-items-center">
                            <a href="{% url 'product_detail' shoe.slug %}" class="btn btn-primary">View Details</a>
                            {% if user.is_authenticated %}
                            <form action="{% url 'add_to_cart' shoe.id %}" method="post" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-success">Add to Cart</button>
                            </form>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-12">
                <p class="text-center">No shoes found.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
""")

    # Create product_detail.html
    with open(template_dir / 'product_detail.html', 'w') as f:
        f.write("""
{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-6">
        <img src="{{ shoe.image.url }}" class="img-fluid" alt="{{ shoe.name }}">
    </div>
    <div class="col-md-6">
        <h2>{{ shoe.name }}</h2>
        <p class="lead"><strong>${{ shoe.price }}</strong></p>
        <p>{{ shoe.description }}</p>
        <p><strong>Category:</strong> {{ shoe.category.name }}</p>
        <p><strong>Stock:</strong> {{ shoe.stock }}</p>
        
        {% if user.is_authenticated %}
        <form action="{% url 'add_to_cart' shoe.id %}" method="post" class="mt-4">
            {% csrf_token %}
            <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input type="number" name="quantity" id="quantity" class="form-control" min="1" max="{{ shoe.stock }}" value="1">
            </div>
            <button type="submit" class="btn btn-success mt-3">Add to Cart</button>
        </form>
        {% else %}
        <p class="mt-4">Please <a href="{% url 'login' %}">login</a> to add this item to your cart.</p>
        {% endif %}
    </div>
</div>
{% endblock %}
""")

    # Create cart.html
    with open(template_dir / 'cart.html', 'w') as f:
        f.write("""
{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-12">
        <h2>Shopping Cart</h2>
        
        {% if cart_items %}
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Subtotal</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in cart_items %}
                    <tr>
                        <td>{{ item.shoe.name }}</td>
                        <td>${{ item.shoe.price }}</td>
                        <td>{{ item.quantity }}</td>
                        <td>${{ item.shoe.price|multiply:item.quantity }}</td>
                        <td>
                            <form action="{% url 'remove_from_cart' item.id %}" method="post" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-danger btn-sm">Remove</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" class="text-end"><strong>Total:</strong></td>
                        <td colspan="2"><strong>${{ total }}</strong></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'shop' %}" class="btn btn-secondary">Continue Shopping</a>
            <a href="{% url 'checkout' %}" class="btn btn-primary">Proceed to Checkout</a>
        </div>
        
        {% else %}
        <p class="text-center">Your cart is empty.</p>
        <div class="text-center">
            <a href="{% url 'shop' %}" class="btn btn-primary">Continue Shopping</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
""")

    # Create checkout.html
    with open(template_dir / 'checkout.html', 'w') as f:
        f.write("""
{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2>Checkout</h2>
        <form action="{% url 'process_checkout' %}" method="post">
            {% csrf_token %}
            <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" class="form-control" id="name" name="name" required>
            </div>
            <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea class="form-control" id="address" name="address" rows="3" required></textarea>
            </div>
            <div class="mb-3">
                <label for="phone" class="form-label">Phone Number</label>
                <input type="tel" class="form-control" id="phone" name="phone" required>
            </div>
            <button type="submit" class="btn btn-primary">Place Order</button>
        </form>
    </div>
    <div class="col-md-4">
        <h3>Order Summary</h3>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Total: ${{ total }}</h5>
                <p class="card-text">Shipping: Free</p>
                <p class="card-text"><strong>Grand Total: ${{ total }}</strong></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

    # Create style.css
    with open(base_dir / 'static' / 'css' / 'style.css', 'w') as f:
        f.write("""
/* General Styles */
body {
    background-color: #f8f9fa;
}

/* Navbar Styles */
.navbar {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
    font-weight: bold;
}

/* Card Styles */
.card {
    transition: transform 0.2s;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-5px);
}

.card-img-top {
    height: 200px;
    object-fit: cover;
}

/* Product Grid Styles */
.product-grid {
    margin-top: 2rem;
}

.product-item {
    margin-bottom: 2rem;
}

/* Button Styles */
.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

/* Footer Styles */
footer {
    margin-top: 4rem;
}

/* Cart Styles */
.cart-item {
    margin-bottom: 1rem;
}

.cart-item:last-child {
    margin-bottom: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
    .navbar-brand {
        font-size: 1.2rem;
    }
    
    .card {
        margin-bottom: 1rem;
    }
}
""")

    # Create main.js
    with open(base_dir / 'static' / 'js' / 'main.js', 'w') as f:
        f.write("""
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
});
""")

def main():
    print("Creating project structure...")
    create_directories()
    print("Creating files...")
    create_files()
    print("Project setup complete!")

if __name__ == '__main__':
    main()
