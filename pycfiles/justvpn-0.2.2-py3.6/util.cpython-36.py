# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/justvpn/util.py
# Compiled at: 2020-05-01 07:39:21
# Size of source mod 2**32: 638 bytes
import re, os
from urllib.parse import urlparse

def encode_url(url):
    if re.match('https?://.+', url) is None:
        url = 'http://' + url
    parsed = urlparse(url)
    if parsed.netloc == 'vpn.just.edu.cn':
        return url
    else:
        path = parsed.path
        if path == '':
            path = '/'
        ssl_flag = ''
        if parsed.scheme == 'https':
            ssl_flag = ',SSL'
        path, filename = os.path.split(path)
        if path[(-1)] != '/':
            path += '/'
        encoded_url = 'https://vpn.just.edu.cn%s,DanaInfo=%s%s+%s?%s' % (
         path, parsed.netloc, ssl_flag, filename, parsed.query)
        return encoded_url