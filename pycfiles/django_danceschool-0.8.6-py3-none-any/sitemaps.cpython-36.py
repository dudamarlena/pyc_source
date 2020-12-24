# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/sitemaps.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 313 bytes
from django.contrib.sitemaps import Sitemap
from .models import Event

class EventSitemap(Sitemap):
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return Event.objects.exclude(status=(Event.RegStatus.hidden))

    def lastmod(self, obj):
        return obj.modified