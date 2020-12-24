# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cifar_extender/cifar_download.py
# Compiled at: 2018-02-20 21:12:23
# Size of source mod 2**32: 2841 bytes
import os, sys, csv, asyncio
from collections import defaultdict
import requests
IMG_DIR = './images/'

def download_images(loop, image_dir, urls, category, n=100):
    """
    download image from url to disk

    :param loop: event loop for the downloading.
    :type loop: asyncio.AbstractEventLoop()
    :param image_dir: key for the image file, used as the file name
    :type image_dir: str
    :param urls: urls for the image files
    :type urls: list
    :param category: categeory for the image, used to save to a class directory
    :type category: str
    :param n: number of pictures to download
    :type n: int
    :return: None
    :rtype: None
    """
    dir_path = os.path.join(image_dir, category)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    for url in urls:
        if len(os.listdir(dir_path)) >= n:
            break
        file_name = url.split('/')[(-1)]
        file_path = os.path.join(dir_path, file_name)
        try:
            image = requests.get(url, allow_redirects=False, timeout=2)
        except Exception as e:
            print(e)
            continue

        print('{}/{} - {}: {}'.format(len(os.listdir(dir_path)) + 1, n, category, file_name))
        headers = image.headers
        if image.status_code != 200:
            print('\tCONNECTION ERROR {}: {}'.format(image.status_code, url))
        else:
            if headers['Content-Type'] != 'image/jpeg':
                print('\tFILE TYPE ERROR {}: {}'.format(headers['Content-Type'], url))
            else:
                if int(headers['Content-Length']) < 50000:
                    print('\tFILE SIZE ERROR {}: {}'.format(headers['Content-Length'], url))
                else:
                    with open(file_path, 'wb') as (file):
                        file.write(image.content)

    loop.stop()


def get_collection(filename):
    collection = defaultdict(list)
    with open(filename, 'r') as (f):
        reader = csv.reader(f)
        for row in reader:
            category, url = row
            collection[category].append(url)

    return collection


def main(datafile, n=100, img_dir=None):
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        if not img_dir:
            img_dir = IMG_DIR
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
    d = get_collection(datafile)
    loop = asyncio.get_event_loop()
    for k in d.keys():
        loop.call_soon(download_images, loop, img_dir, d[k], k, n)

    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main('data/images.csv', n=100)