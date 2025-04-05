import os
import shutil
import datetime
import requests
from bs4 import BeautifulSoup

# Configurable parameters
start_date = "250404"  # Format: YYMMDD (e.g., 250404 for April 4, 2025)
num_days = 20  # Number of days to retrieve

# Base URL
base_url = "https://apod.nasa.gov/apod/ap"

def generate_urls(start_date, num_days):
    # Convert start_date to datetime object
    start_date_obj = datetime.datetime.strptime(start_date, "%y%m%d")

    urls = []
    for i in range(num_days):
        # Calculate the previous date
        previous_date = start_date_obj - datetime.timedelta(days=i)
        formatted_date = previous_date.strftime("%y%m%d")
        
        # Construct the URL
        url = f"{base_url}{formatted_date}.html"
        urls.append(url)
    
    return urls

def fetch_AOPD_with_URL(url):
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML to find the image URL and title
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find('img')  # Locate the image
    title_tag = soup.find('b')    # APOD's title is typically bolded (first <b> tag)

    if image_tag:
        image_url = "https://apod.nasa.gov/apod/" + image_tag['src']
        image_title = title_tag.text.strip() if title_tag else "Untitled_APOD"
        return image_url, image_title
    else:
        raise ValueError('No valid image found on the APOD page.')

def save_image(folder, image_url, image_title):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    # Generate a valid file name
    safe_title = image_title.replace(' ', '_').replace('/', '_')
    image_file = os.path.join(folder, f"{safe_title}.jpg")

    # Save the image
    with open(image_file, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    return image_file

# Generate URLs
urls = generate_urls(start_date, num_days)

# Fetch and save images
for url in urls:
    try:
        image_url, image_title = fetch_AOPD_with_URL(url)
        save_image("NASAPOD_Images", image_url, image_title)
        print(f"Image saved: {image_title} ({image_url})")
    except Exception as e:
        print(f"Error fetching from {url}: {e}")