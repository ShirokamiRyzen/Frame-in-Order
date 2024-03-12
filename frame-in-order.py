#! /usr/bin/env python3
import requests
import urllib3
import signal
import sys
import os
import logging
import argparse
import time
import random

signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))
urllib3.disable_warnings()

# Menghitung jumlah file di direktori frames
frame_loop = len([name for name in os.listdir('frames') if os.path.isfile(os.path.join('frames', name))])

# Ambil semua nama file dalam direktori frames
file_names = os.listdir('frames')

# Ekstrak nomor frame dari nama file dan simpan dalam daftar
frame_numbers = [int(name.split('.')[0]) for name in file_names]

# Ambil nilai maksimum dari daftar nomor frame
frame_count = max(frame_numbers)

parser = argparse.ArgumentParser()
parser.add_argument('--start', metavar='123', type=int, help='First frame you want to upload')

# Mengubah nilai default loop
parser.add_argument('--loop', metavar=str(frame_loop), nargs='?', default=frame_loop, type=int, help='Loop value')
args = parser.parse_args()
frame_start = args.start
loopvalue = args.loop

class color:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   reset = '\033[0m'

if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
elif frame_start == None:
        parser.print_help(sys.stderr)
        print()
        print(f"{color.red}{color.bold}Error! First frame value is mandatory{color.reset}{color.reset}")
        sys.exit(1)

logging.basicConfig(level=logging.DEBUG)
# User your access token
ACCESS_TOKEN = ''
url = "https://graph.facebook.com/v5.0/me/photos"
x = frame_start
y = loopvalue
first_run = True  # Menandai apakah ini adalah run pertama atau tidak
for i in range(x, min(x + y, frame_count + 1)):
    if not first_run:
        delay = random.randint(30, 90)  # Tunggu waktu acak antara 30 hingga 90 detik setiap kali, kecuali run pertama
        time.sleep(delay)
    num = (f"{i:0>4}")
    image_source = (f"./frames/{num}.png")
    caption = (f"Charlotte Episode 1 [Frame {num}/{frame_count}]")
    payload = {
        'access_token' : ACCESS_TOKEN,
        'caption': caption, 
        'published' : 'true',
    }
    files = {'source': (image_source, open(image_source, 'rb'))}
    r = requests.post(url, files=files, data=payload)
    if r.status_code == 200:
        logging.debug(f"{color.bold}{color.green}Frame {num} Uploaded{color.reset}. {r.json()}")
        os.remove(f"{image_source}")
    else:
        logging.debug(f"{color.bold}{color.red}Failed to Upload Frame {num}{color.reset}. {r.json()}")
        break
    first_run = False  # Setelah run pertama, ubah menjadi False
print(f"{color.bold}Task Done{color.reset}")