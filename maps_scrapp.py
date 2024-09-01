import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import random
import string
# List of Google Maps URLs to scrape
urls = [
    "https://maps.app.goo.gl/m42xPGAiieo9RbFm9",
    "https://www.google.com/maps/place/Ezeiza/"
]
def randomName(longitud):
    caracteres = string.ascii_letters + string.digits  # Letras y dígitos
    string_aleatorio = ''.join(random.choice(caracteres) for _ in range(longitud))
    return string_aleatorio

def scrape_google_maps_image(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_tag = soup.find('meta', property="og:image")
        if meta_tag:
            image_url = meta_tag['content']
            
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            image = Image.open(BytesIO(img_response.content))
            
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            image_name = f"image_{randomName(5)}.jpg"
            image.save(image_name)
            print(f"Image saved as {image_name}")
            return image_name, url
        else:
            print(f"No image found for {url}")
            return None
        print(f"Error scraping {url}: {e}")
        return None
    except OSError as e:
        print(f"Error processing image for {url}: {e}")
        return None



for url in urls:
    result = scrape_google_maps_image(url)
    if result:
        image_name, scraped_url = result
        print(f"Scraped image: {image_name} from {scraped_url}")
