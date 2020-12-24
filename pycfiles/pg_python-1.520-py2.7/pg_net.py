# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/pg_python/pg_net.py
# Compiled at: 2019-03-05 03:55:08
from urllib.parse import urlparse

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = ('{uri.netloc}/').format(uri=parsed_uri).strip('/')
    return domain


def get_proper_domain(url):
    d = get_domain(url)
    prefix_remove = ['http://', 'https://', 'www.']
    for prefix in prefix_remove:
        if d.startswith(prefix):
            d = d[len(prefix):]

    return d