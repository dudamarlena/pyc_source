# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/znbstatic/znbstatic/utils.py
# Compiled at: 2019-01-07 16:14:59
# Size of source mod 2**32: 600 bytes
from django.utils.six.moves.urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

def add_version_to_url(url, version):
    url_parts = urlparse(url)
    query = parse_qsl(url_parts.query)
    query.append(('v', version))
    return urlunparse(url_parts[:4] + (urlencode(query),) + url_parts[5:])