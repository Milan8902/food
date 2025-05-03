from django.core.management.base import BaseCommand
from shoes.models import Shoe, Size, ShoeSize

class Command(BaseCommand):
    help = 'Fix shoe size data'

    def handle(self, *args, **options):
        # Create sizes if they don't exist
        sizes = [
            {'size': '6', 'description': 'Size 6'},
            {'size': '7', 'description': 'Size 7'},
            {'size': '8', 'description': 'Size 8'},
            {'size': '9', 'description': 'Size 9'},
            {'size': '10', 'description': 'Size 10'},
            {'size': '11', 'description': 'Size 11'},
            {'size': '12', 'description': 'Size 12'}
        ]

        # Create sizes if they don't exist
        for size_data in sizes:
            size, created = Size.objects.get_or_create(
                size=size_data['size'],
                defaults={'description': size_data['description']}
            )

        # Get all shoes
        shoes = Shoe.objects.all()

        # Create ShoeSize instances with initial stock
        for shoe in shoes:
            # First delete existing ShoeSize entries for this shoe
            ShoeSize.objects.filter(shoe=shoe).delete()
            
            # Then create new ones
            for size in Size.objects.all():
                # Create ShoeSize with random stock between 0 and 50
                stock = 0 if shoe.stock == 0 else min(shoe.stock, 50)
                ShoeSize.objects.create(
                    shoe=shoe,
                    size=size,
                    stock=stock
                )

        self.stdout.write(self.style.SUCCESS('Successfully fixed shoe size data'))
