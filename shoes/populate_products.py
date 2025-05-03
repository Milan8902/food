import os
import requests
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.core.management.base import BaseCommand
from shoes.models import Category, Shoe, Size

class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Men', 'description': 'Men\'s Shoes', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff'},
            {'name': 'Women', 'description': 'Women\'s Shoes', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff'},
            {'name': 'Kids', 'description': 'Kids\'s Shoes', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff'}
        ]

        # Create sizes
        sizes = [
            {'size': '6'},
            {'size': '7'},
            {'size': '8'},
            {'size': '9'},
            {'size': '10'},
            {'size': '11'},
            {'size': '12'}
        ]

        # Create sample products
        products = [
            {
                'name': 'Air Jordan 1 Retro High OG',
                'description': 'The Air Jordan 1 Retro High OG returns with its classic design and premium materials.',
                'price': 199.99,
                'category': 'Men',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
                'sizes': ['9', '10', '11']
            },
            {
                'name': 'Air Jordan 3 Retro',
                'description': 'The Air Jordan 3 Retro features the iconic elephant print and classic design.',
                'price': 189.99,
                'category': 'Men',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
                'sizes': ['9', '10', '11']
            },
            {
                'name': 'Air Jordan 4 Retro',
                'description': 'The Air Jordan 4 Retro combines classic design with modern comfort.',
                'price': 199.99,
                'category': 'Men',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
                'sizes': ['9', '10', '11']
            },
            {
                'name': 'Air Jordan 1 Mid',
                'description': 'The Air Jordan 1 Mid offers a mid-top silhouette with classic AJ1 styling.',
                'price': 149.99,
                'category': 'Women',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
                'sizes': ['6', '7', '8']
            },
            {
                'name': 'Air Jordan 1 Low',
                'description': 'The Air Jordan 1 Low provides a low-top option with iconic AJ1 design.',
                'price': 139.99,
                'category': 'Kids',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
                'sizes': ['6', '7', '8']
            }
        ]

        def download_image(url):
            response = requests.get(url)
            return BytesIO(response.content)

        # Create categories
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            
            # Download and save category image
            if created and 'image_url' in category_data:
                image_data = download_image(category_data['image_url'])
                category.image.save(f'{category.name.lower()}_category.jpg', File(image_data))

        # Create sizes
        for size_data in sizes:
            Size.objects.get_or_create(size=size_data['size'])

        # Create products
        for product_data in products:
            # Get or create category
            category = Category.objects.get(name=product_data['category'])
            
            # Create product
            product = Shoe.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=category,
                stock=50,
                is_featured=True
            )
            
            # Download and save product image
            image_data = download_image(product_data['image_url'])
            product.image.save(f'{product.name.lower().replace(" ", "_")}.jpg', File(image_data))
            
            # Add sizes
            for size_str in product_data['sizes']:
                size = Size.objects.get(size=size_str)
                product.sizes.add(size)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample products'))
