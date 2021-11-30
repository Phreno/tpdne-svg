#!/usr/bin/python3
"""
Use bash to download a file with this command

curl 'https://thispersondoesnotexist.com/image' \
  -H 'authority: thispersondoesnotexist.com' \
  -H 'sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
  -H 'if-none-match: "6161db77-6a883"' \
  -H 'if-modified-since: Sat, 09 Oct 2021 18:12:07 GMT' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-dest: image' \
  -H 'referer: https://thispersondoesnotexist.com/' \
  -H 'accept-language: fr-FR,fr;q=0.9,de-DE;q=0.8,de;q=0.7,en-US;q=0.6,en;q=0.5,eo;q=0.4' \
  --compressed
"""

import os
import sys
import time
import random
import argparse
import requests
from pathlib import Path
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

parser = argparse.ArgumentParser(description='Download random images from thispersondoesnotexist.com')
parser.add_argument('-n', '--number', type=int, default=100, help='number of images to download')
parser.add_argument('-o', '--output', type=str, default='images', help='output directory')
parser.add_argument('-s', '--sleep', type=int, default=0, help='sleep time between requests')
args = parser.parse_args()


def download_image(url):
    """
    Download an image from thispersondoesnotexist.com
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def main():
    """
    Main function
    """
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a pool of threads
    pool = ThreadPool(4)

    # Download images
    for i in range(args.number):
        url = 'https://thispersondoesnotexist.com/image'
        image = download_image(url)
        if image is not None:
            # Save image
            filename = '{}.jpg'.format(i)
            with open(output_dir / filename, 'wb') as f:
                f.write(image)
            print('[+] {}'.format(filename))
        else:
            print('[-] {}'.format(filename))
        time.sleep(args.sleep)


if __name__ == '__main__':
    main()