# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: googlesearch/googlesearch.py
# Compiled at: 2017-09-07 02:22:45
from __future__ import print_function
import re, traceback, sys
from random import choice
from data import user_agents
try:
    from urllib import request
    from html.parser import HTMLParser
    from html import unescape
    from urllib.parse import quote
except ImportError:
    import urllib2 as request
    from urllib import quote
    from HTMLParser import HTMLParser

isPython2 = sys.version.startswith('2')

def download(query, num_results):
    """
        downloads HTML after google search
        """
    name = quote(query)
    name = name.replace(' ', '+')
    url = 'http://www.google.com/search?q=' + name
    if num_results != 10:
        url += '&num=' + str(num_results)
    req = request.Request(url, headers={'User-Agent': choice(user_agents)})
    try:
        response = request.urlopen(req)
    except Exception:
        print('ERROR\n')
        traceback.print_exc()
        return ''

    if isPython2:
        data = response.read().decode('utf8', errors='ignore')
    else:
        data = str(response.read(), 'utf-8', errors='ignore')
    return data


def is_url(url):
    """
        checks if :url is a url
        """
    regex = '((https?):((//)|(\\\\\\\\))+([\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&](#!)?)*)'
    return re.match(regex, url) is not None


def prune_html(text):
    """
        https://stackoverflow.com/a/42461722/2295672
        """
    text = re.sub('<.*?>', '', text)
    return text


def convert_unicode(text):
    """
        converts unicode HTML to real Unicode
        """
    if isPython2:
        h = HTMLParser()
        s = h.unescape(text)
    else:
        s = unescape(text)
    return s


def search(query, num_results=10):
    """
        searches google for :query and returns a list of tuples
        of the format (name, url)
        """
    data = download(query, num_results)
    results = re.findall('\\<h3.*?\\>.*?\\<\\/h3\\>', data, re.IGNORECASE)
    if results is None or len(results) == 0:
        print('No results where found? Did the rate limit exceed?')
        return []
    else:
        links = []
        for r in results:
            mtch = re.match('.*?a\\s*?href=\\"(.*?)\\".*?\\>(.*?)\\<\\/a\\>.*$', r, flags=re.IGNORECASE)
            if mtch is None:
                continue
            url = mtch.group(1)
            url = re.sub('^.*?=', '', url, count=1)
            url = re.sub('\\&amp.*$', '', url, count=1)
            name = prune_html(mtch.group(2))
            name = convert_unicode(name)
            if is_url(url):
                links.append((name, url))

        return links


def run():
    """
        CLI endpoint to run the program
        """
    if len(sys.argv) > 1:
        print(search(sys.argv[1]))
    else:
        print(search('君の名'))


if __name__ == '__main__':
    run()