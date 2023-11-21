import requests
import re
import time
import random
import sys
import os
from tqdm import tqdm

logo= """
┏┓┏┓┳┓┏┓•┏┓┏┓┳┓    ┓ ┏┓
┗┓┃ ┣┫┣┫┓┃┃┣ ┣┫  ┓┏┃ ┃┃
┗┛┗┛┛┗┛┗┗┣┛┗┛┛┗  ┗┛┻•┗╋
By Kallamamran

"""

print(logo)

#----------------------------------------------------------------------------------
# Function to download images with a progress bar
def download_image(image_url, filename, current, total):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url, stream=True, allow_redirects=True)
        # Check if the request was successful
        if response.status_code == 200:
            # Get the total file size from headers
            file_size = int(response.headers.get('content-length', 0))
            # Open the file in binary write mode
            with open(filename, 'wb') as file, tqdm(
                desc=f"Downloading image {current}/{total}",
                total=file_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                # Download the file in chunks
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
                        # Update the progress bar
                        bar.update(len(chunk))
            return True
    except requests.RequestException as e:
        print(f"Failed to download image {filename}. Error: {e}")
    return False
#----------------------------------------------------------------------------------

search_term = input('Enter the search term for the images: ')
desired_image_count = int(input('Enter the number of images you want to download: '))

# Get input from user and use a default value if input is blank
img_per_page_input = input('Enter the amount of images you want the scraper to load per page (leave blank to use 20): ')
img_per_page = int(img_per_page_input) if img_per_page_input.isdigit() else 20

download_location = input('Enter foldername you want to create for your downloads (leave blank to use your search term): ')

# If download location is left blank, use the search term as the folder name
if not download_location:
    download_location = search_term
   

# Ensure download location ends with a slash and exists
download_location = download_location.rstrip('/') + '/'
if download_location and not os.path.exists(download_location):
    os.makedirs(download_location)

downloaded_images = 0
current_page = 1
errors = 0
max_errors = 10

try:
    while downloaded_images < desired_image_count:
        # Fetch the search results page
        api_url = f'https://unsplash.com/napi/search/photos?query={search_term}&page={current_page}&per_page=20'
        response = requests.get(api_url)

        if response.status_code == 200:
            images_data = response.json()
            # If no more images are found, break the loop
            if not images_data['results']:
                print('No more images to download.')
                break

            for photo in images_data['results']:
                if downloaded_images >= desired_image_count:
                    break

                photo_id = photo['id']
                filename = os.path.join(download_location, f'{search_term}_{photo_id}.jpg')

                # Only attempt to download if the file doesn't already exist
                if not os.path.exists(filename):
                    download_url = photo['links']['download']
                    if download_image(download_url, filename, downloaded_images + 1, desired_image_count):
                        downloaded_images += 1
                        errors = 0  # Reset the error count after a successful download
                    else:
                        errors += 1
                        if errors >= max_errors:
                            print("Too many consecutive errors, stopping the script.")
                            break  # Breaking out of the inner loop
                else:
                    print(f"Image already exists: {filename}")
                    continue  # Skip to the next photo

            if errors >= max_errors:
                break  # Breaking out of the outer loop if max errors reached

            current_page += 1
            # Random delay between 1.0 and 5.0 seconds
            time.sleep(random.uniform(1.0, 2.0))
        else:
            print(f"Failed to retrieve page {current_page}: Status code {response.status_code}")
            errors += 1
            if errors >= max_errors:
                print("Too many consecutive errors, stopping the script.")
                break  # Breaking out of the outer loop

            # Random delay before retrying
            time.sleep(random.uniform(1.0, 2.0))

except KeyboardInterrupt:
    print('\nScript interrupted by user. Exiting gracefully.')
    sys.exit(0)
