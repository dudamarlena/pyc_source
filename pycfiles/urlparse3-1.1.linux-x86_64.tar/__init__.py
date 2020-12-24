# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/urlparse3/__init__.py
# Compiled at: 2014-11-02 15:28:57
"""
Urlparse3 is simple and powerful url parsing tool.
Url must conform RFC 3986. Scheme is required and must be followed be colon.
Example usage:

import urlparse3

url = "http://domain.com/path/?id=1&id=2#anchor"
parsed_url = urlparse3.parse_url(url)
print parsed_url.query["id"]  # ["1", "2"]
parsed_url.query["name"] = "alex"
# get url back to string representation
print parsed_url.geturl()  # "http://domain.com/path/?id=1&id=2&name=alex#anchor"
"""
from .urlparse3 import parse_url, ParsedUrl