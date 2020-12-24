# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\absolute_uri.py
# Compiled at: 2013-08-27 09:59:12
from __future__ import unicode_literals
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from django.contrib.sites.models import get_current_site

def add_domain(path, domain, secure=False):
    if path.startswith(b'http://') or path.startswith(b'https://'):
        return path
    domain = (b'https://' if secure else b'http://') + domain
    return urljoin(domain, path)


def build_site_url(path, request=None):
    current_site = get_current_site(request=request)
    domain = current_site.domain
    secure = request.is_secure() if request is not None else False
    return add_domain(path, domain, secure=secure)