# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/sitemaps.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import unicode_literals
from django.contrib.sitemaps import Sitemap
from wenlincms.core.models import Displayable

class DisplayableSitemap(Sitemap):
    Sitemap.limit = 20000

    def items(self):
        return list(Displayable.objects.url_map().values())

    def get_urls(self, **kwargs):
        return super(DisplayableSitemap, self).get_urls(**kwargs)