#!/usr/bin/env python3


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
import subprocess
from pathlib import Path
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from file_tools import render_svg

parser = argparse.ArgumentParser(
    description='Download images from thispersondoesnotexist.com')
parser.add_argument('--threads', type=int, default=1,
                    help='Number of threads to use')
parser.add_argument('--output', type=str, default='images',
                    help='Output directory')
parser.add_argument('--start', type=int, default=1, help='Start index')
parser.add_argument('--end', type=int, default=100, help='End index')
parser.add_argument('--timeout', type=int, default=10,
                    help='Timeout for each request')
parser.add_argument('--retry', type=int, default=3,
                    help='Number of retries for each request')
parser.add_argument('--sleep', type=int, default=0,
                    help='Sleep time between each request')
parser.add_argument('--verbose', action='store_true', help='Verbose mode')
args = parser.parse_args()


def download(index):
    url = 'https://thispersondoesnotexist.com/image'
    headers = {
        'authority': 'thispersondoesnotexist.com',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'if-none-match': '"6161db77-6a883"',
        'if-modified-since': 'Sat, 09 Oct 2021 18:12:07 GMT',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'image',
        'referer': 'https://thispersondoesnotexist.com/',
        'accept-language': 'fr-FR,fr;q=0.9,de-DE;q=0.8,de;q=0.7,en-US;q=0.6,en;q=0.5,eo;q=0.4',
    }
    for i in range(args.retry):
        try:
            response = requests.get(url, headers=headers, timeout=args.timeout)
            if response.status_code == 200:
                with open(os.path.join(args.output, f'{index}.jpg'), 'wb') as f:
                    f.write(response.content)
                if args.verbose:
                    print(f'[{index}] Downloaded')
                return
        except Exception as e:
            if args.verbose:
                print(f'[{index}] Error: {e}')
            time.sleep(args.sleep)
    if args.verbose:
        print(f'[{index}] Failed')


def convert(index):
    """
    Foreach downloaded pictures, make an svg using potrace
    """
    render_svg(f'./images/{index}.jpg')


if __name__ == '__main__':
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    pool = ThreadPool(args.threads)
    pool.map(download, range(args.start, args.end + 1))
    pool.close()
    pool.join()
    pool = ThreadPool(args.threads)
    pool.map(convert, range(args.start, args.end + 1))
    pool.close()
    pool.join()
