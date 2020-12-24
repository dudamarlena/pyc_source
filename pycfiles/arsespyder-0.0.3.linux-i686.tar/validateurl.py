# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pyarsespyder/validateurl.py
# Compiled at: 2013-09-22 14:18:23
from urlparse import urlparse

def url_is_http(url):
    """ 
    This functions checks if url has HTTP/HTTPS scheme 
   
    Keyword arguments:
    url -- A string with the URL to analyze

    """
    parsed = urlparse(url)
    if parsed.scheme and (parsed.scheme == 'http' or parsed.scheme == 'https'):
        return True
    return False