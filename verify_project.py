import os
from pathlib import Path

def verify_project_structure():
    base_dir = Path(__file__).resolve().parent
    
    # Check directories
    required_dirs = [
        'static',
        'staticcss',
        'staticjs',
        'staticimages',
        'templates',
        'shoe_shop',
        'shoes'
    ]
    
    print("\nVerifying project structure...")
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name} directory exists")
        else:
            print(f"✗ {dir_name} directory does not exist")
    
    # Check required files
    required_files = [
        'manage.py',
        'requirements.txt',
        'README.md',
        'templates/base.html',
        'staticcss/style.css',
        'staticjs/main.js'
    ]
    
    print("\nVerifying required files...")
    for file_path in required_files:
        if (base_dir / file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} does not exist")

if __name__ == '__main__':
    verify_project_structure()
