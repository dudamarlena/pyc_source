# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazyscraper/urltools.py
# Compiled at: 2018-01-14 15:45:40
import json, hashlib, csv, logging, sys
from urllib.request import urlopen
from urllib.parse import urljoin
import requests, lxml.html, lxml.etree
from .consts import *
try:
    from bmemcached import Client
    from zlib import compress, decompress
except:
    pass

def get_cached_post(url, postdata, host='127.0.0.1', port=11211):
    """Returns url data from url with post request"""
    servers = [
     '%s:%d' % (host, port)]
    m = hashlib.sha256()
    m.update(url.encode('utf8'))
    m.update(str(postdata).encode('utf8'))
    key = m.hexdigest()
    client = Client(servers)
    c_data = client.get(key)
    if c_data:
        data = decompress(c_data)
    else:
        r = requests.post(url, postdata)
        data = r.text
        client.set(key, compress(data))
    hp = lxml.etree.HTMLParser(encoding='utf-8')
    root = lxml.html.fromstring(data, parser=hp)
    return root


def get_cached_url(url, timeout=DEFAULT_CACHE_TIMEOUT, host='127.0.0.1', port=11211):
    """Returns url data from url or from local memcached"""
    servers = [
     '%s:%d' % (host, port)]
    m = hashlib.sha256()
    m.update(url.encode('utf8'))
    key = m.hexdigest()
    client = Client(servers)
    c_data = client.get(key)
    if c_data:
        data = decompress(c_data)
    else:
        o = urlopen(url)
        rurl = o.geturl()
        data = o.read()
        client.set(key, compress(data))
    hp = lxml.etree.HTMLParser(encoding='utf-8')
    root = lxml.html.fromstring(data, parser=hp)
    return root