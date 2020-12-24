# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hmacauth/client/authenticated_request.py
# Compiled at: 2017-07-26 11:26:21
# Size of source mod 2**32: 949 bytes
from tornado.httpclient import HTTPRequest
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from hmacauth.digest import generate_digest

def authenticated_request(*args, **kwargs):
    hmac_key = kwargs.pop('hmac_key')
    hmac_secret = kwargs.pop('hmac_secret')
    if len(args) > 0:
        url = args[0]
    else:
        if 'url' in kwargs:
            url = kwargs['url']
        else:
            raise TypeError("Missing argument: 'url'")
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query
    body = kwargs.get('body', '')
    if isinstance(body, str):
        body = body.encode('utf-8')
    digest = generate_digest(hmac_secret, kwargs.get('method', 'GET'), path, query, body)
    headers = kwargs.get('headers', {})
    headers['Authorization'] = 'USTUDIO-HMAC-V2 {} {}'.format(hmac_key, digest)
    kwargs['headers'] = headers
    return HTTPRequest(*args, **kwargs)