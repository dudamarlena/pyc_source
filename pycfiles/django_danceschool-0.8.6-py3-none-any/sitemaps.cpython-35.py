# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/sitemaps.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 313 bytes
from django.contrib.sitemaps import Sitemap
from .models import Event

class EventSitemap(Sitemap):
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return Event.objects.exclude(status=Event.RegStatus.hidden)

    def lastmod(self, obj):
        return obj.modified