# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/views.py
# Compiled at: 2019-09-27 06:15:57
# Size of source mod 2**32: 1161 bytes
from urllib.parse import urljoin, urlparse
from flask import request, session, url_for

def next_redirect(fallback_endpoint, *args, **kwargs):
    """Find redirect url. The order of search is request params, session and
    finally url for fallback endpoint is returned if none found. Args and
    kwargs are passed intact to endpoint.

    :param fallback_endpoint: full endpoint specification
    :type fallback_endpoint: str
    :return: HTTP path to redirect to
    :rtype: str
    """
    return is_redirect_safe(request.args.get('next')) or is_redirect_safe(session.pop('next', None)) or url_for(fallback_endpoint, *args, **kwargs)


def is_redirect_safe(target):
    """Check if redirect is safe, that is using HTTP protocol and is pointing
    to the same site.

    :param target: redirect target url
    :type target: str
    :return: flag signalling whether redirect is safe
    :rtype: bool
    """
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc