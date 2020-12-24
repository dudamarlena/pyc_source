# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/sitemap.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 306 bytes
from django.contrib.sitemaps import Sitemap
from .models import CMSEntries

class CMSEntriesSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return CMSEntries.objects.filter(published=True)

    def lastmod(self, item):
        return item.date_modified