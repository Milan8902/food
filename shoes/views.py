from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from .models import Category, Shoe, Cart, CartItem, Size, ShoeSize, ProductComparison, Review
from django.db.models import Q
from django.utils import timezone

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
    
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        shoes = shoes.filter(category=category)
    
    search_query = request.GET.get('q')
    if search_query:
        shoes = shoes.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    context = {
        'categories': categories,
        'shoes': shoes,
        'selected_category': category_slug
    }
    return render(request, 'shop.html', context)

def product_detail(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    
    # Get available sizes for this shoe
    available_sizes = ShoeSize.objects.filter(shoe=shoe, stock__gt=0)
    
    # Get compared products for logged-in users
    compared_products = []
    if request.user.is_authenticated:
        comparisons = ProductComparison.objects.filter(user=request.user)
        compared_products = [comp.shoe for comp in comparisons]
    
    # Calculate original price as 20% more than current price
    original_price = shoe.price * Decimal('1.20')
    
    return render(request, 'product_detail.html', {
        'shoe': shoe,
        'available_sizes': available_sizes,
        'compared_products': compared_products,
        'original_price': original_price
    })

@login_required
def cart(request):
    cart = None
    cart_items = []
    total = 0
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        for item in cart_items:
            total += item.shoe.price * item.quantity
    
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, shoe_id):
    try:
        shoe = get_object_or_404(Shoe, id=shoe_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        size_id = request.POST.get('size')
        if not size_id:
            messages.error(request, 'Please select a size')
            return redirect('shoes:product_detail', shoe.slug)
        
        size = get_object_or_404(Size, id=size_id)
        shoe_size = get_object_or_404(ShoeSize, shoe=shoe, size=size)
        
        if shoe_size.stock <= 0:
            messages.error(request, 'This size is out of stock')
            return redirect('shoes:product_detail', shoe.slug)
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1')
            return redirect('shoes:product_detail', shoe.slug)
        
        if quantity > shoe_size.stock:
            messages.error(request, f'Only {shoe_size.stock} items available')
            return redirect('shoes:product_detail', shoe.slug)
        
        # Check if item already exists in cart
        cart_item = CartItem.objects.filter(
            cart=cart,
            shoe=shoe,
            size=size
        ).first()
        
        if cart_item:
            # Update existing item
            new_quantity = cart_item.quantity + quantity
            if new_quantity > shoe_size.stock:
                messages.error(request, f'Only {shoe_size.stock} items available')
                return redirect('shoes:product_detail', shoe.slug)
            
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Updated quantity to {new_quantity} {shoe.name}')
        else:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                shoe=shoe,
                size=size,
                quantity=quantity
            )
            messages.success(request, f'Added {quantity} {shoe.name} to cart')
        
        # Update stock
        shoe_size.stock -= quantity
        shoe_size.save()
        
        return redirect('shoes:cart')
        
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('shoes:product_detail', shoe.slug)

@login_required
def add_to_comparison(request, shoe_id):
    try:
        shoe = get_object_or_404(Shoe, id=shoe_id)
        
        # Check if product is already in comparison
        if ProductComparison.objects.filter(user=request.user, shoe=shoe).exists():
            return JsonResponse({'success': False, 'message': 'Product already in comparison'})
        
        comparison = ProductComparison.objects.create(
            user=request.user,
            shoe=shoe
        )
        
        shoe.compared_count += 1
        shoe.save()
        
        return JsonResponse({'success': True, 'message': 'Product added to comparison'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

@login_required
def remove_from_comparison(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    ProductComparison.objects.filter(user=request.user, shoe=shoe).delete()
    return redirect('shoes:compare_products')

def compare_products(request):
    if request.user.is_authenticated:
        comparisons = ProductComparison.objects.filter(user=request.user)
        compared_products = [comp.shoe for comp in comparisons]
    else:
        compared_products = []
    
    return render(request, 'compare_products.html', {
        'compared_products': compared_products
    })

@login_required
def add_review(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        
        # Create or update review
        review, created = Review.objects.get_or_create(
            shoe=shoe,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.updated_at = timezone.now()
            review.save()
        
        # Update shoe's average rating
        reviews = Review.objects.filter(shoe=shoe)
        total_rating = sum(review.rating for review in reviews)
        shoe.rating = total_rating
        shoe.rating_count = reviews.count()
        shoe.save()
        
        messages.success(request, 'Thank you for your review!')
        return redirect('shoes:product_detail', shoe.slug)
    
    return redirect('shoes:product_detail', shoe.slug)

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    # Update stock
    shoe_size = get_object_or_404(ShoeSize, shoe=cart_item.shoe, size=cart_item.size)
    shoe_size.stock += cart_item.quantity
    shoe_size.save()
    
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('shoes:cart')

@login_required
def checkout(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.shoe.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Process checkout
        for item in cart_items:
            # Create order items
            # This is where you would typically create an Order and OrderItem
            # For now, we'll just clear the cart
            item.delete()
        
        if request.method == 'POST':
            # Process the order
            total = sum(item.shoe.price * item.quantity for item in cart_items)
            # Here you would typically create an order object and process payment
            messages.success(request, 'Order placed successfully!')
            # Clear the cart
            cart_items.delete()
            return redirect('home')
            
        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'total': sum(item.shoe.price * item.quantity for item in cart_items)
        })
    except Cart.DoesNotExist:
        messages.error(request, 'No active cart found')
        return redirect('home')
