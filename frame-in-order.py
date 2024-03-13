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
        os.remove(image_source)
    else:
        logging.debug(f"\033[1m\033[91mFailed to Upload Frame {num}\033[0m\033[0m. {r.json()}")
        break
    
    first_run = False

print("\033[1mTask Done\033[0m")
