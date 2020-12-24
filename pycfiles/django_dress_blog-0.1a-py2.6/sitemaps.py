# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/sitemaps.py
# Compiled at: 2012-07-20 05:27:44
import datetime
from django.contrib.sitemaps import Sitemap
from dress_blog.models import Post

class PostsSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Post.objects.filter(status__gte=2, pub_date__lte=datetime.datetime.now()).order_by('-pub_date')

    def lastmod(self, obj):
        return obj.mod_date