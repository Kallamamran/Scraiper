import requests
import re
import time
import random
import sys
import os
from tqdm import tqdm

logo= """
┏┓┏┓┳┓┏┓┏┓┏┓┳┓    ┓ ┏━
┗┓┃ ┣┫┣┫┃┃┣ ┣┫  ┓┏┃ ┗┓
┗┛┗┛┛┗┛┗┣┛┗┛┛┗  ┗┛┻•┗┛
By Kallamamran

"""

print(logo)

#----------------------------------------------------------------------------------
# Function to download images with a progress bar
def download_image(image_url, filename, current, total):
    try:
        with requests.get(image_url, stream=True, allow_redirects=True) as response:
            if response.status_code == 200:
                file_size = int(response.headers.get('content-length', 0))
                with open(filename, 'wb') as file, tqdm(
                    desc=f"Downloading image {current}/{total}",
                    total=file_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            file.write(chunk)
                            bar.update(len(chunk))
                return True
            else:
                print(f"Failed to download image {filename}. HTTP Status Code: {response.status_code}")
                return False
    except requests.RequestException as e:
        print(f"Failed to download image {filename}. Request Exception: {e}")
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
        api_url = f'https://unsplash.com/napi/search/photos?query={search_term}&page={current_page}&per_page={img_per_page}'
        response = requests.get(api_url)

        if response.status_code == 200:
            images_data = response.json()
            if not images_data['results']:
                print('No more images to download.')
                break

            for photo in images_data['results']:
                if downloaded_images >= desired_image_count:
                    break

                # Check if the image is marked as premium or plus
                if photo.get('premium', False) or photo.get('plus', False):
                    print(f"Skipping premium/plus image: {photo['id']}")
                    continue

                photo_id = photo['id']
                download_url = photo['links']['download']  # Set download URL
                filename = os.path.join(download_location, f'{search_term}_{photo_id}.jpg')

                if not os.path.exists(filename):
                    # Attempt to download the image
                    if download_image(download_url, filename, downloaded_images + 1, desired_image_count):
                        downloaded_images += 1  # Increment downloaded images count
                        errors = 0  # Reset the error count after a successful download
                        time.sleep(random.uniform(1.0, 2.0))  # Sleep after each iteration
                    else:
                        errors += 1  # Increment the error count only after a failed download attempt
                        print(f"An error occurred after attempting to download. Error count: {errors}")
                        if errors >= max_errors:
                            print(f"Too many consecutive errors [{errors}], stopping the script.")
                            time.sleep(random.uniform(1.0, 2.0))  # Sleep after each iteration
                            break  # Break out of the inner loop
                else:
                    print(f"Skipping download - {filename} already exists")

                if errors >= max_errors:
                    break  # Break out of the outer loop if max errors reached

            current_page += 1

        else:
            print(f"Failed to retrieve page {current_page}: Status code {response.status_code}")
            errors += 1
            if errors >= max_errors:
                print("Too many consecutive errors, stopping the script.")
                break  # Breaking out of the outer loop

except KeyboardInterrupt:
    print('\nScript interrupted by user. Exiting gracefully.')
    sys.exit(0)
