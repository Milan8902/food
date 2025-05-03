import os
import requests
from PIL import Image
from io import BytesIO

# Create images directory if it doesn't exist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(os.path.join(IMAGES_DIR, 'products'), exist_ok=True)
os.makedirs(os.path.join(IMAGES_DIR, 'categories'), exist_ok=True)

# List of image URLs for different product types
image_urls = {
    'hero': 'https://images.unsplash.com/photo-1574301368179-5798950769b2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1920&q=80',
    'shoes': [
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
    ],
    'categories': [
        'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
    ]
}

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Create Image object from response
        img = Image.open(BytesIO(response.content))
        
        # Save the image
        img.save(filename)
        print(f"Successfully downloaded {filename}")
        
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# Download hero image
hero_filename = os.path.join(IMAGES_DIR, 'hero.jpg')
download_image(image_urls['hero'], hero_filename)

# Download product images
for i, url in enumerate(image_urls['shoes']):
    product_filename = os.path.join(IMAGES_DIR, 'products', f'product_{i+1}.jpg')
    download_image(url, product_filename)

# Download category images
for i, url in enumerate(image_urls['categories']):
    category_filename = os.path.join(IMAGES_DIR, 'categories', f'category_{i+1}.jpg')
    download_image(url, category_filename)

print("Image download complete!")
