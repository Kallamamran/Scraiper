# Scraiper
My first unsplash scraper or really my first Python project ever, so be nice 😉

Being my first code ever I have of course had "some" help creating it, so thank you GPT for your valueable input 😊

This script will download the high resolution version of images found on Unsplash and put them in a folder of your choice for further use. I've made this to make it easier downloading regularization images for Dreambooth training of checkpoints for Stable Diffusion. The images will of course need some further processing after downloading such as removing unsuitable images, resizing and cropping. Dr. Furkan (https://www.patreon.com/SECourses/) has some EXCELLENT scripts for this and he also actually gave me the idea for this script.
I only found a limited amount of working scrapers for Unsplash and they all relied on the API (which is probably better, but what the hell). Now, at least I learned some Python ;)

1. Run it by running "python.exe scrape_v1.4.py"
2. It will ask for a search term used to find the images you want to download. For example "dog"
3. It will ask for the amount of images you want to download and keep downloading until this number is reached or until it has reached the end of the search results.
4. It will ask for the amount of images per page that you want to load. Defaults to 20, but you can change this if you know why you're doing it 😉
5. It will ask for a foldername (Leaving it blank will use the search term from 1.)

Existing images will not be overwritten and will not count as downloads.
