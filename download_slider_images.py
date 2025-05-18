import requests
import os
from PIL import Image
from io import BytesIO

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Open the image and resize it
            img = Image.open(BytesIO(response.content))
            img = img.resize((1920, 500), Image.Resampling.LANCZOS)
            
            # Save the resized image
            img.save(filename, quality=85, optimize=True)
            print(f"Downloaded and processed {filename}")
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Create slider directory if it doesn't exist
os.makedirs("public/images/slider", exist_ok=True)

# List of eco-friendly images to download
images = [
    {
        "url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09",
        "filename": "public/images/slider/eco1.jpg"
    },
    {
        "url": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b",
        "filename": "public/images/slider/eco2.jpg"
    },
    {
        "url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f",
        "filename": "public/images/slider/eco3.jpg"
    }
]

# Download and process each image
for img in images:
    download_image(img["url"], img["filename"]) 