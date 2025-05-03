import os
import re

def update_static_paths():
    template_dir = 'templates'
    
    # Update base.html
    with open(os.path.join(template_dir, 'base.html'), 'r') as f:
        content = f.read()
    
    # Update CSS path
    content = re.sub(r'{% static \'css/style.css\' %}', '{% static \'staticcss/style.css\' %}', content)
    
    # Update JS path
    content = re.sub(r'{% static \'js/main.js\' %}', '{% static \'staticjs/main.js\' %}', content)
    
    with open(os.path.join(template_dir, 'base.html'), 'w') as f:
        f.write(content)
    
    print("Updated static file paths in base.html")

if __name__ == '__main__':
    update_static_paths()
