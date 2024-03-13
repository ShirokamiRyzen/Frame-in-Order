import requests
import urllib3
import signal
import sys
import os
import logging
import argparse
import time
import random
import json
from PIL import Image

urllib3.disable_warnings()

# Load configuration from external file
def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

# Function to check if config.json exists
def config_exists():
    return os.path.isfile("config.json")

# Signal handler
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--start', metavar='123', type=int, help='First frame you want to upload')
parser.add_argument('--loop', metavar='n', type=int, help='Loop value')
args = parser.parse_args()

# Load configuration from file if config.json exists
if config_exists():
    config = load_config("config.json")
else:
    print("Configuration file 'config.json' is required.")
    sys.exit(1)

# Initialize variables from configuration
ACCESS_TOKEN = config.get('ACCESS_TOKEN', '')
MIN_DELAY = config.get('MIN_DELAY', 180)
MAX_DELAY = config.get('MAX_DELAY', 240)
TITLE_EPS = config.get('TITLE_EPS', '')

# Set default loop value
frame_loop = len([name for name in os.listdir('frames') if os.path.isfile(os.path.join('frames', name))])

# Extract frame numbers from file names
file_names = os.listdir('frames')
frame_numbers = [int(name.split('.')[0]) for name in file_names]
frame_count = max(frame_numbers)

# Validate command line arguments
if len(sys.argv)==1 or args.start is None:
    parser.print_help(sys.stderr)
    print()
    print("\033[91m\033[1mError! First frame value is mandatory\033[0m\033[0m")
    sys.exit(1)

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Facebook Graph API URL
url = "https://graph.facebook.com/v5.0/me/photos"

def save_cropped_frame(image, crop_x, crop_y, crop_width, crop_height):
    if not os.path.exists('crop_frames'):
        os.makedirs('crop_frames')
    
    # Generate a new file path for the cropped image
    file_name = f"crop_{crop_width}x{crop_height}_{os.path.basename(image.filename)}"
    cropped_image_path = os.path.join('crop_frames', file_name)
    
    # Create and save the cropped image
    cropped_image = image.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
    cropped_image.save(cropped_image_path)
    
    return cropped_image_path

def get_random_crop_coordinates(image):
    # Determine the minimum and maximum crop size
    min_crop_size = 350
    max_crop_size = 480
    
    # Generate random crop dimensions
    crop_width = random.randint(min_crop_size, max_crop_size)
    crop_height = random.randint(min_crop_size, max_crop_size)
    
    # Generate random crop position
    max_x = image.width - crop_width
    max_y = image.height - crop_height
    
    crop_x = random.randint(0, max_x)
    crop_y = random.randint(0, max_y)
    
    return crop_x, crop_y, crop_width, crop_height

def random_crop_comment(post_id, image, crop_x, crop_y, crop_width, crop_height):
    # Save the cropped image to the "crop_frames" folder
    cropped_image_path = save_cropped_frame(image, crop_x, crop_y, crop_width, crop_height)

    caption = f"Random Crop. [{crop_width}x{crop_height} ~ X: {crop_x}, Y: {crop_y}]"
    
    # Open the cropped image
    with open(cropped_image_path, 'rb') as cropped_image_file:
        files = {'source': cropped_image_file}
        payload = {
            'access_token': ACCESS_TOKEN,
            'message': caption,
        }
        
        r = requests.post(f"https://graph.facebook.com/v5.0/{post_id}/comments", files=files, data=payload)
    
    if r.status_code == 200:
        logging.debug(f"\033[1m\033[92mRandom Crop Comment Uploaded\033[0m\033[0m. {r.json()}")
        # Remove the cropped image after successfully posting
        os.remove(cropped_image_path)
    else:
        logging.debug(f"\033[1m\033[91mFailed to Upload Random Crop Comment\033[0m\033[0m. {r.json()}")

# Main loop for uploading frames
x = args.start
y = args.loop if args.loop else frame_loop
first_run = True

# Iterate through frames
for i in range(x, min(x + y, frame_count + 1)):
    if not first_run:
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)
    
    num = f"{i:0>4}"
    image_source = f"./frames/{num}.png"
    caption = f"{TITLE_EPS} [Frame {num}/{frame_count}]"
    
    payload = {
        'access_token' : ACCESS_TOKEN,
        'caption': caption, 
        'published' : 'true',
    }
    
    files = {'source': (image_source, open(image_source, 'rb'))}
    r = requests.post(url, files=files, data=payload)
    
    if r.status_code == 200:
        logging.debug(f"\033[1m\033[92mFrame {num} Uploaded\033[0m\033[0m. {r.json()}")
        response_json = r.json()
        post_id = response_json.get('post_id')
        
        # Open the image file
        image = Image.open(image_source)
        
        # Get random crop coordinates
        crop_x, crop_y, crop_width, crop_height = get_random_crop_coordinates(image)
        
        # Add random crop comment after uploading frame
        random_crop_comment(post_id, image, crop_x, crop_y, crop_width, crop_height)

        image.close()
        os.remove(image_source)
    else:
        logging.debug(f"\033[1m\033[91mFailed to Upload Frame {num}\033[0m\033[0m. {r.json()}")
        break
    
    first_run = False

print("\033[1mTask Done\033[0m")
