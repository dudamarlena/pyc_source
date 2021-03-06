# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/whtsky/Documents/codes/Catsup/catsup/themes/utils.py
# Compiled at: 2017-10-14 05:20:17
# Size of source mod 2**32: 924 bytes
try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen, HTTPError

import ujson
from catsup.logger import logger

def search_github(name):
    repo_name = 'catsup-theme-{name}'.format(name=name)
    url = 'https://api.github.com/search/repositories?q=' + repo_name
    request = Request(url)
    request.add_header('User-Agent', 'Catsup Theme Finder')
    try:
        response = urlopen(request)
    except HTTPError as e:
        logger.warning('Error when connecting to GitHub: {}'.format(e.msg))
        return

    content = response.read()
    json = ujson.loads(content)
    if json['total_count'] == 0:
        return
    for item in json['items']:
        if item['name'] == repo_name:
            return {'name':item['name'], 
             'clone_url':item['clone_url']}