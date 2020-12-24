# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: redrum/redrum.py
# Compiled at: 2017-11-05 03:38:20
from __future__ import print_function
import sys, requests
from requests.exceptions import ConnectionError
import logging, random, math, os, shutil, subprocess, json, argparse
from .version import __version__
from datetime import datetime, timedelta
from configparser import SafeConfigParser
module_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)

def logistic_function(x, midpoint, k):
    return 1 / (1 + pow(math.e, -k * (x - midpoint)))


def score_image(image, max_views):
    image_ratio = float(image['width']) / image['height']
    if screen_ratio < image_ratio:
        ratio_score = screen_ratio / image_ratio
    else:
        ratio_score = image_ratio / screen_ratio
    views_score = float(image['views']) / max_views
    width_score = float(image['width']) / screen_width
    height_score = float(image['height']) / screen_height
    if width_score > 1:
        width_score = 1
    if height_score > 1:
        height_score = 1
    pixel_score = width_score * height_score
    ratio_logistic_score = logistic_function(ratio_score, ratio_midpoint, ratio_k)
    views_logistic_score = logistic_function(views_score, views_midpoint, views_k)
    pixel_logistic_score = logistic_function(pixel_score, pixel_midpoint, pixel_k)
    final_score = ratio_logistic_score * views_logistic_score * pixel_logistic_score
    return [
     final_score,
     ratio_score,
     views_score,
     pixel_score,
     ratio_logistic_score,
     views_logistic_score,
     pixel_logistic_score]


def get_images(subreddits):
    results = []
    for subreddit in subreddits:
        page_num = 0
        while page_num < max_pages:
            page_url = url.format(subreddit, page_num)
            print(('Indexing page #{0} from subreddit {1}\r').format(page_num, subreddit), end='')
            response = requests.get(page_url, headers=headers).json()
            if response['success'] == True:
                page_results = response['data']
                page_num += 1
                if len(page_results) == 0:
                    break
                results += page_results
            else:
                logging.error(('Received error from Imgur: {0}').format(response['data']['error']))

        if page_num == 0:
            logging.error(('No results found for subreddit {0}.').format(subreddit))
        print()

    print('Unpacking albums')
    images = []
    for result in results:
        if result['is_album']:
            album_id = result['id']
            logging.debug(('Unpacking album {0}').format(album_id))
            response = requests.get(album_url.format(album_id), headers=headers).json()
            album_results = response['data']
            for image in album_results['images']:
                images.append(image)

        else:
            images.append(result)

    images = [ image for image in images if image['width'] > 0 and image['height'] > 0 ]
    if sfw_only:
        images = [ image for image in images if image['nsfw'] == False ]
    if len(images) == 0:
        print('No results found')
        sys.exit()
    print(('Scoring {} images').format(len(images)))
    max_views = max([ image['views'] for image in images ])
    for image in images:
        image['redrum_score'] = score_image(image, max_views)[0]

    return images


def weighted_select(images, seen):
    if unseen_only:
        images = [ image for image in images if image['id'] not in seen ]
    if len(images) == 0:
        print('No images available.  Set `unseen_only` to False, increase `max_pages` or add more subreddits')
        sys.exit()
    total_redrum_score = sum([ image['redrum_score'] for image in images ])
    rand_score = random.uniform(0, total_redrum_score)
    for image in images:
        rand_score -= image['redrum_score']
        if rand_score <= 0:
            break

    print(('Selected {0} ({1}) with score {2} out of {3} images').format(image['link'], image['section'], image['redrum_score'], len(images)))
    print(('The probability of selecting this image was {0}').format(image['redrum_score'] / total_redrum_score))
    return image


def set_wallpaper(image):
    print('Applying wallpaper')
    try:
        response = requests.get(image['link'])
        if response.status_code == 200:
            with open(image_file, 'wb') as (f):
                f.write(response.content)
        else:
            logging.error(('Got response {} when downloading image.').format(reponse.status_code))
    except ConnectionError:
        logging.error('Connection error')
        sys.exit()

    try:
        subprocess.check_output(wallpaper_command.format(image_file=image_file), shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(('Command `{}` failed with status {}').format(e.cmd, e.returncode))
        sys.exit()


def save(images, date, seen, options):
    if not os.path.exists(cache_file):
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'w') as (cache):
        cache.write(json.dumps({'date': date, 'options': options, 
           'seen': seen, 
           'images': images}, indent=4))


parser = argparse.ArgumentParser(description='Reddit wallpaper grabber.')
parser.add_argument('-v', '--version', action='version', version=__version__, help='show version information')
parser.add_argument('--refresh', action='store_true', default=False, help='force a cache refresh')
parser.add_argument('--noset', action='store_true', default=False, help="don't select and set and set wallpaper")
parser.add_argument('--config', action='store_true', default=os.path.expanduser('~/.config/redrum.ini'), help='use a different config path')
args = parser.parse_args()
config_parser = SafeConfigParser()
config_parser.read(args.config)
config = config_parser['redrum']
screen_width = config.getint('screen_width', 1600)
screen_height = config.getint('screen_height', 900)
screen_ratio = float(screen_width) / screen_height
subreddits = config.get('subreddits').split('\n')
sfw_only = config.getboolean('sfw_only', True)
unseen_only = config.getboolean('unseen_only', True)
ratio_midpoint = config.getfloat('ratio_midpoint', 0.95)
views_midpoint = config.getfloat('views_midpoint', 0.75)
pixel_midpoint = config.getfloat('pixel_midpoint', 1)
ratio_k = config.getfloat('ratio_k', 15)
views_k = config.getfloat('views_k', 15)
pixel_k = config.getfloat('pixel_k', 15)
max_pages = config.getint('max_pages', 5)
url = config.get('url', 'https://api.imgur.com/3/gallery/r/{0}/top/all/{1}')
album_url = config.get('album_url', 'https://api.imgur.com/3/album/{0}')
client_id = config.get('client_id', '5f21952153b5f6c')
headers = {'Authorization': ('Client-ID {0}').format(client_id)}
cache_file = os.path.expanduser(config.get('cache_file', '~/.cache/redrum_cache.json'))
image_file = os.path.expanduser(config.get('image_file', '~/.cache/redrum_image'))
wallpaper_command = config.get('wallpaper_command', 'feh --bg-scale {image_file}')
cache_expiry = timedelta(days=7)
date_format = '%a %b %d %H:%M:%S %Y'
options = [
 sfw_only, subreddits, screen_width, screen_height, ratio_midpoint,
 views_midpoint, pixel_midpoint, ratio_k, views_k, pixel_k, max_pages, url]

def main():
    if not os.path.exists(cache_file):
        print(('No previous score cache found at {0}.').format(cache_file))
        date = datetime.strftime(datetime.now(), date_format)
        images = get_images(subreddits)
        seen = []
    else:
        with open(cache_file, 'r') as (cache):
            j = json.loads(cache.read())
            print(('Found cache at {0}').format(cache_file))
            date = j['date']
            cache_age = datetime.now() - datetime.strptime(date, date_format)
            if cache_age > cache_expiry or j['options'] != options or args.refresh:
                print('Refreshing cache...')
                images = get_images(subreddits)
                date = datetime.now().strftime(date_format)
            else:
                images = j['images']
        seen = j['seen']
    if not args.noset:
        image = weighted_select(images, seen)
        set_wallpaper(image)
        seen.append(image['id'])
    save(images, date, seen, options)


if __name__ == '__main__':
    main()