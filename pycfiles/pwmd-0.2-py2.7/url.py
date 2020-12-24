# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/pwmd/url.py
# Compiled at: 2012-12-17 22:29:26
from urllib import unquote
from urlparse import urlparse
try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

def _parse_url(url):
    scheme = urlparse(url).scheme
    schemeless = url[len(scheme) + 3:]
    parts = urlparse('http://' + schemeless)
    port = scheme != 'mongodb' and parts.port or None
    hostname = schemeless if scheme == 'mongodb' else parts.hostname
    path = parts.path or ''
    path = path[1:] if path and path[0] == '/' else path
    return (scheme, unquote(hostname or '') or None, port,
     unquote(parts.username or '') or None,
     unquote(parts.password or '') or None,
     unquote(path or '') or None,
     dict(parse_qsl(parts.query)))


def parse_url(url):
    scheme, host, port, user, password, db, query = _parse_url(url)
    return dict(transport=scheme, host=host, port=port, user=user, password=password, db=db, **query)