# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/sitemaps/tests/urls/https.py
# Compiled at: 2018-07-11 18:15:31
from django.conf.urls import patterns
from .http import SimpleSitemap

class HTTPSSitemap(SimpleSitemap):
    protocol = 'https'


secure_sitemaps = {'simple': HTTPSSitemap}
urlpatterns = patterns('django.contrib.sitemaps.views', (
 '^secure/index\\.xml$', 'index', {'sitemaps': secure_sitemaps}), (
 '^secure/sitemap-(?P<section>.+)\\.xml$', 'sitemap', {'sitemaps': secure_sitemaps}))