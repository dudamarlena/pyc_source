# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_net.py
# Compiled at: 2018-08-03 06:01:13
# Size of source mod 2**32: 381 bytes
from urlparse import urlparse

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}/'.format(uri=parsed_uri).strip('/')
    return domain


def get_proper_domain(url):
    d = get_domain(url)
    prefix_remove = ['http://', 'https://', 'www.']
    for prefix in prefix_remove:
        if d.startswith(prefix):
            d = d[len(prefix):]

    return d