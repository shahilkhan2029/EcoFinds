import os
import requests
from PIL import Image
from io import BytesIO

# Create products directory if it doesn't exist
os.makedirs('public/images/products', exist_ok=True)

# Image URLs for each product
image_urls = {
    # Category images
    'recycled-products.jpg': 'https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=800&h=600&fit=crop',
    'organic-products.jpg': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800&h=600&fit=crop',
    'upcycled-items.jpg': 'https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=800&h=600&fit=crop',
    'eco-furniture.jpg': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&h=600&fit=crop',
    'sustainable-fashion.jpg': 'https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=800&h=600&fit=crop',
    'natural-beauty.jpg': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=600&fit=crop',
    
    # Product images
    'recycled-glass-vase.jpg': 'https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=800&h=600&fit=crop',
    'recycled-notebook.jpg': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800&h=600&fit=crop',
    'organic-tshirt.jpg': 'https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=800&h=600&fit=crop',
    'organic-soap.jpg': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=600&fit=crop',
    'upcycled-bag.jpg': 'https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=800&h=600&fit=crop',
    'upcycled-shelf.jpg': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&h=600&fit=crop'
}

def download_and_resize_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Open image from response content
            img = Image.open(BytesIO(response.content))
            
            # Resize image to 800x600 while maintaining aspect ratio
            img.thumbnail((800, 600))
            
            # Save image
            img.save(f'public/images/products/{filename}', 'JPEG', quality=85)
            print(f'Successfully downloaded and saved {filename}')
        else:
            print(f'Failed to download {filename}: HTTP {response.status_code}')
    except Exception as e:
        print(f'Error processing {filename}: {str(e)}')

def main():
    for filename, url in image_urls.items():
        download_and_resize_image(url, filename)

if __name__ == '__main__':
    main() 