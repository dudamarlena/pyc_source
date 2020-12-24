# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/requestbin/tools.py
# Compiled at: 2015-02-18 16:02:39
"""
common tools module
"""

def normalize_url(url):
    """remove stacked forward slashes and trailing slash"""
    import re
    return re.sub('([^:])///*', '\\1/', url).rstrip('/')


def pathjoin(*parts, **kvs):
    """join path parts into a path; in case url is not none, use that, too"""
    url = kvs.pop('url', '/')
    url = url + '/' + ('/').join(parts)
    url = normalize_url(url)
    return url