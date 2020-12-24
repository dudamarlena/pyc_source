# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/parser.py
# Compiled at: 2016-02-11 09:18:14
import json, re
from bs4 import BeautifulSoup
from oauth_tokens.models import AccessToken
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0', 
   'Accept_Language': 'en'}
IDS_RE = re.compile('data-tweet-id="(\\d+)"')

def get_replies(status):
    """Return all replies ids of tweet"""
    replies_ids = set()
    url = 'https://twitter.com/i/%s/conversation/%s' % (status.author.screen_name, status.pk)
    ar = AccessToken.objects.get_token('twitter').auth_request
    headers = dict(HEADERS)
    headers['X-Requested-With'] = 'XMLHttpRequest'
    resp = ar.authorized_request(url=status.get_url(), headers=headers)
    params = {'max_position': BeautifulSoup(resp.content).find('div', **{'class': 'stream-container'})['data-min-position']}
    while True:
        r = ar.authorized_request(url=url, params=params, headers=headers)
        response = r.json()
        if 'descendants' in response:
            response = response['descendants']
        ids = IDS_RE.findall(response['items_html'])
        [ replies_ids.add(id) for id in ids ]
        if response['has_more_items'] and len(ids):
            params = {'max_position': response['min_position']}
        else:
            break

    return list(replies_ids)