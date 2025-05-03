import os
import django
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_shop.settings')
application = get_wsgi_application()

from shoes.models import Category, Shoe

def create_sample_data():
    # Create categories
    categories = [
        'Sports',
        'Casual',
        'Formal',
        'Running',
        'Sneakers'
    ]

    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        if created:
            print(f"Created category: {category_name}")

    # Create sample shoes
    sample_shoes = [
        {
            'name': 'Running Pro',
            'description': 'High-performance running shoes for professional athletes',
            'price': 150.00,
            'category': 'Running',
            'stock': 50,
            'is_featured': True
        },
        {
            'name': 'Casual Walker',
            'description': 'Comfortable everyday walking shoes',
            'price': 89.99,
            'category': 'Casual',
            'stock': 100,
            'is_featured': False
        },
        {
            'name': 'Formal Classic',
            'description': 'Elegant formal shoes for business occasions',
            'price': 129.99,
            'category': 'Formal',
            'stock': 75,
            'is_featured': True
        }
    ]

    for shoe_data in sample_shoes:
        category = Category.objects.get(name=shoe_data['category'])
        shoe = Shoe.objects.create(
            name=shoe_data['name'],
            description=shoe_data['description'],
            price=shoe_data['price'],
            category=category,
            stock=shoe_data['stock'],
            is_featured=shoe_data['is_featured']
        )
        print(f"Created shoe: {shoe.name}")

if __name__ == '__main__':
    create_sample_data()
