# E-commerce Shoe Shop

A modern e-commerce website built with Django for selling shoes.

## Features
- Product catalog with shoe listings
- Shopping cart functionality
- User authentication
- Product categories and filtering
- Responsive design with Bootstrap
- Admin panel for managing products

## Setup Instructions
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
- `shoes/` - Main app containing models, views, and templates
- `static/` - Contains CSS, JavaScript, and images
- `templates/` - HTML templates for the website
- `media/` - User-uploaded files
