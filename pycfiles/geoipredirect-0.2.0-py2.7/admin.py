# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/geoip/admin.py
# Compiled at: 2011-01-25 05:00:10
from django.contrib import admin
from geoip.models import GeoIPRecord, IPRedirectEntry, IgnoreURL
admin.site.register(GeoIPRecord)
admin.site.register(IPRedirectEntry)
admin.site.register(IgnoreURL)