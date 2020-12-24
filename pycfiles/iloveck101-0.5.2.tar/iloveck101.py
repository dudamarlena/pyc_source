# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tzangms/projects/iloveck101/iloveck101/iloveck101.py
# Compiled at: 2013-12-02 22:32:29
import os, sys, re, requests
from lxml import etree
from iloveck101.utils import get_image_info

def iloveck101(url):
    """
    download images from given ck101 URL
    """
    m = re.match('thread-(\\d+)-.*', url.rsplit('/', 1)[1])
    if not m:
        sys.exit('URL pattern should be something like this: http://ck101.com/thread-2593278-1-1.html')
    thread_id = m.group(1)
    home = os.path.expanduser('~')
    base_folder = os.path.join(home, 'Pictures/iloveck101')
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)
    for attemp in range(3):
        resp = requests.get(url)
        if resp.status_code != 200:
            print 'Retrying ...'
            continue
        html = etree.HTML(resp.content)
        try:
            title = html.find('.//title').text.split(' - ')[0].replace('/', '').strip()
            break
        except AttributeError:
            print 'Retrying ...'
            continue

    folder = os.path.join(base_folder, '%s - %s' % (thread_id, title))
    if not os.path.exists(folder):
        os.mkdir(folder)
    image_urls = html.xpath('//img/@file')
    for image_url in image_urls:
        filename = image_url.rsplit('/', 1)[1]
        if not image_url.startswith('http'):
            continue
        print 'Fetching %s ...' % image_url
        resp = requests.get(image_url)
        content_type, width, height = get_image_info(resp.content)
        if width < 400 or height < 400:
            continue
        with open(os.path.join(folder, filename), 'wb+') as (f):
            f.write(resp.content)


def main():
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit('Please provide URL from ck101')

    iloveck101(url)


if __name__ == '__main__':
    main()