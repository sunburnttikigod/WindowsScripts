
import os
import requests
import shutil

# NASA API key and endpoint
API_KEY = 'pY6Uu9tp9B3lUl6YHdIVAefs3853Zx4i9cLd1T3d'
APOD_URL = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'

# Folder paths
BY_DATE_FOLDER = 'NasaTopTenByDate'
MY_TOP_TEN_FOLDER = 'MyNasaTopTen'

# Function to fetch NASA's Image of the Day
def fetch_image_of_the_day():
    response = requests.get(APOD_URL)
    response.raise_for_status()
    data = response.json()

    # Ensure the image is not video content
    if data.get('media_type') == 'image':
        return data['url'], data['title']
    else:
        raise ValueError('Image of the Day is not a valid image.')

# Function to save image to a folder
def save_image(folder, image_url, image_title):
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    # Generate a valid file name
    image_file = os.path.join(folder, f"{image_title.replace(' ', '_').replace('/', '_')}.jpg")
    with open(image_file, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    return image_file

# Function to keep a folder at capacity 10
def maintain_folder_capacity(folder):
    files = sorted(os.listdir(folder), key=lambda x: os.path.getctime(os.path.join(folder, x)))
    while len(files) > 10:
        os.remove(os.path.join(folder, files.pop(0)))

# Main script execution
try:
    image_url, image_title = fetch_image_of_the_day()

    # Add image to NasaTopTenByDate folder
    save_image(BY_DATE_FOLDER, image_url, image_title)
    maintain_folder_capacity(BY_DATE_FOLDER)

    # User moderation for MyNasaTopTen can be done manually
    print(f"Image '{image_title}' saved in '{BY_DATE_FOLDER}'.")
    print(f"Please review and add the image manually to '{MY_TOP_TEN_FOLDER}' if desired.")

except Exception as e:
    print(f"An error occurred: {e}")