from django.core.management.base import BaseCommand
from shoes.models import Category, Shoe, Size
import requests
from io import BytesIO
from django.core.files import File

class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Men', 'description': 'Men\'s Shoes'},
            {'name': 'Women', 'description': 'Women\'s Shoes'},
            {'name': 'Kids', 'description': 'Kids\'s Shoes'}
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
