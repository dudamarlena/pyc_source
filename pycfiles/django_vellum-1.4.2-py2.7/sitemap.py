# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/sitemap.py
# Compiled at: 2012-04-05 15:23:29
from django.contrib.sitemaps import Sitemap
from vellum.models import Post

class BlogSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Post.objects.published()

    def lastmod(self, obj):
        return obj.publish