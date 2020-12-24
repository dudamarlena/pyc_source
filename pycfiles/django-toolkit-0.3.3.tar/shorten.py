# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/ahayes/data/.workspaces/juno/django-toolkit/django_toolkit/url/shorten.py
# Compiled at: 2015-06-30 21:51:25
from __future__ import absolute_import
from __future__ import print_function
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import tldextract

def shorten_url(url, length=32, strip_www=True, strip_path=True, ellipsis=False):
    """
    Shorten a URL by chopping out the middle.

    For example if supplied with http://subdomain.example.com.au and length 16
    the following would be returned.

    sub...le.com.au
    """
    if '://' not in url:
        url = 'http://%s' % url
    parsed_url = urlparse(url)
    ext = tldextract.extract(parsed_url.netloc)
    if ext.subdomain and (not strip_www or strip_www and ext.subdomain != 'www'):
        shortened = '%s.%s' % (ext.subdomain, ext.domain)
    else:
        shortened = '%s' % ext.domain
    if ext.tld:
        shortened = '%s.%s' % (shortened, ext.tld)
    if not strip_path:
        if parsed_url.path:
            shortened += parsed_url.path
    if len(shortened) <= length:
        return shortened
    else:
        domain = shortened
        i = length + 1 - 3
        left = right = int(i / 2)
        if not i % 2:
            right -= 1
        if ellipsis:
            shortened = '%s…%s' % (domain[:left], domain[-right:])
        else:
            shortened = '%s...%s' % (domain[:left], domain[-right:])
        return shortened


def netloc_no_www(url):
    """
    For a given URL return the netloc with any www. striped.
    """
    ext = tldextract.extract(url)
    if ext.subdomain and ext.subdomain != 'www':
        return '%s.%s.%s' % (ext.subdomain, ext.domain, ext.tld)
    else:
        return '%s.%s' % (ext.domain, ext.tld)