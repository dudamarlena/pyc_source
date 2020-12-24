# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/webutil.py
# Compiled at: 2017-04-03 12:49:00
# Size of source mod 2**32: 3187 bytes
"""
Various utilities for HTTP-related activities.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import codecs, six
try:
    from http import cookiejar
except ImportError:
    import cookielib as cookiejar

try:
    from urllib import error, parse, request
except ImportError:
    import urrlib2 as error, urrlib2 as parse, urrlib2 as request

from .util import *
__all__ = str('\nHTMLParser\nHTTPError\nbuild_opener\nget_url_from_redirection\nparse_http_html\nurlencode\nurljoin\nurlopen\nurlparse\nurlquote\nurlunparse\nurlunquote\n').split()
build_opener = request.build_opener
urlencode = parse.urlencode
HTTPError = error.HTTPError
urlquote = parse.quote
urlunquote = parse.unquote
urlopen = request.urlopen
try:
    from urllib.parse import urljoin, urlparse, urlunparse
except ImportError:
    from urlparse import urljoin, urlparse, urlunparse

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

class NonRedirectingProcessor(request.HTTPErrorProcessor):

    def http_response(self, request, response):
        return response

    https_response = http_response


class DebugRedirectHandler(request.HTTPRedirectHandler):
    __doc__ = "Shouldn't be used in production code, but useful for proxy debugging."

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        import sys
        print('REDIRECT:', (req.get_method()), code, newurl, file=(sys.stderr))
        return request.HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, headers, newurl)


def get_url_from_redirection(url):
    """Note that we don't go through the proxy class here for convenience, under
    the assumption that all of these redirections involve public information
    that won't require privileged access."""
    opener = request.build_opener(NonRedirectingProcessor())
    resp = opener.open(url)
    if resp.code not in (301, 302, 303, 307) or 'Location' not in resp.headers:
        die("expected a redirection response for URL %s but didn't get one", url)
    resp.close()
    return resp.headers['Location']


def parse_http_html(resp, parser):
    """`parser` need only have two methods: `feed()` and `close()`."""
    debug = False
    if six.PY2:
        charset = resp.headers.getparam('charset')
    else:
        charset = resp.headers.get_content_charset('ISO-8859-1')
    if charset is None:
        charset = 'ISO-8859-1'
    dec = codecs.getincrementaldecoder(charset)()
    if debug:
        f = open('debug.html', 'w')
    while True:
        d = resp.read(4096)
        if not len(d):
            text = dec.decode(b'', final=True)
            parser.feed(text)
            break
        if debug:
            f.write(d)
        text = dec.decode(d)
        parser.feed(text)

    if debug:
        f.close()
    resp.close()
    parser.close()
    return parser