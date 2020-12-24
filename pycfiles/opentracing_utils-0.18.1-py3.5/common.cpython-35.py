# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opentracing_utils/common.py
# Compiled at: 2019-02-13 08:31:21
# Size of source mod 2**32: 754 bytes
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import urllib.parse as parse

def sanitize_url(url, mask_url_query=True, mask_url_path=False):
    parsed = parse.urlsplit(url)
    host = '{}:{}'.format(parsed.hostname, parsed.port) if parsed.port else parsed.hostname
    query = str(parse.urlencode({k:'?' for k in parse.parse_qs(parsed.query).keys()})) if mask_url_query else parsed.query
    path = '/??/' if parsed.path and mask_url_path else parsed.path
    components = parse.SplitResult(parsed.scheme, host, path, query, parsed.fragment)
    return parse.urlunsplit(components)