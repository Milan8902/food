from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg

class Size(models.Model):
    size = models.CharField(max_length=10)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.size

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
    sizes = models.ManyToManyField(Size, through='ShoeSize')
    image = models.ImageField(upload_to='shoe_images/')
    stock = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    compared_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    rating_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        if self.rating_count > 0:
            return round(self.rating / self.rating_count, 1)
        return 0.0

    @property
    def rating_percentage(self):
        return (self.average_rating / 5) * 100

class ShoeSize(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    class Meta:
        unique_together = ('shoe', 'size')

    def __str__(self):
        return f"{self.shoe.name} - Size {self.size.size}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        size_str = f"Size {self.size.size}" if self.size else "No Size"
        return f"{self.quantity} x {self.shoe.name} - {size_str} in cart {self.cart.id}"

class ProductComparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'shoe')

    def __str__(self):
        return f"{self.user.username} - {self.shoe.name}"

class Review(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.shoe.name} - {self.rating} stars"
