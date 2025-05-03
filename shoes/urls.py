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
    path('compare/', views.compare_products, name='compare_products'),
    path('add-to-comparison/<int:shoe_id>/', views.add_to_comparison, name='add_to_comparison'),
    path('remove-from-comparison/<int:shoe_id>/', views.remove_from_comparison, name='remove_from_comparison'),
    path('add-review/<int:shoe_id>/', views.add_review, name='add_review'),
    path('add-review/<int:shoe_id>/', views.add_review, name='add_review'),
]
