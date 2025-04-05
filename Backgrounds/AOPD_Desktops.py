# Charlie Must
# 2025-04-04
# This script fetches the Astronomy Picture of the Day (APOD) from NASA's website 
# for a specified date range. It saves the images to a local folder and ensures 
# that the folder does not exceed a specified number of images. The script uses 
# BeautifulSoup for HTML parsing and requests for HTTP requests.
# I use it to dump their beautiful images to my desktop background slideshow folder

import os
import shutil
import datetime
import requests
from bs4 import BeautifulSoup

# Configurable parameters
start_date = "250404"                                                           ## Format: YYMMDD (e.g., 250404 for April 4, 2025)
num_days = 20                                                                   ## Number of days to retrieve

# Base URL
base_url = "https://apod.nasa.gov/apod/ap"

# Function to generate URLs for the specified date range
def generate_urls(start_date, num_days):
    start_date_obj = datetime.datetime.strptime(start_date, "%y%m%d")           ## Convert string to datetime object
    urls = []                                                                   ## Initialize an empty list to store URLs 
    for i in range(num_days):                                                   ## Loop through the number of days
        # Calculate the previous date
        previous_date = start_date_obj - datetime.timedelta(days=i)             ## Subtract days from the start date
        formatted_date = previous_date.strftime("%y%m%d")                       ## Format the date as YYMMDD
        
        # Construct the URL
        url = f"{base_url}{formatted_date}.html"                                ## Construct the URL using the formatted date
        urls.append(url)                                                        ## Append the URL to the list
    
    return urls                                                                 ## Return the list of URLs

# Function to fetch the APOD image URL and title from the HTML page
def fetch_AOPD_with_URL(url):
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML to find the image URL and title
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find('img')                                                ## Locate the image
    title_tag = soup.find('b')                                                  ## APOD's title is typically bolded (first <b> tag)

    if image_tag:
        image_url = "https://apod.nasa.gov/apod/" + image_tag['src']            ## Construct the full image URL
        image_title = title_tag.text.strip() if title_tag else "Untitled_APOD"  ## Extract the title text
        return image_url, image_title                                           ## If no image tag is found, check for a video or other media type  
    else:
        raise ValueError('No valid image found on the APOD page.')              ## If no image tag is found, check for a video or other media type

# Function to save the image to a specified folder
def save_image(folder, image_url, image_title):
    # Ensure the folder exists
    if not os.path.exists(folder):                                              ## Check if the folder exists
        os.makedirs(folder)                                                     ## Create the folder if it doesn' t exist

    # Fetch the image
    response = requests.get(image_url, stream=True)                             ## Stream the image content 
    response.raise_for_status()                                                 ## Check for successful response    

    # Generate a valid file name
    safe_title = image_title.replace(' ', '_').replace('/', '_')                ## Replace spaces and slashes with underscore
    image_file = os.path.join(folder, f"{safe_title}.jpg")                      ## Create a valid file name 

    # Save the image
    with open(image_file, 'wb') as f:                                           ## Open the file in binary write mode
        shutil.copyfileobj(response.raw, f)                                     ## Copy the image content to the file
    return image_file                                                           ## Return the file path

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