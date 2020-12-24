# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/djangopypi/admin.py
# Compiled at: 2015-10-27 08:49:00
from django.conf import settings
from django.contrib import admin
from djangopypi.models import *
admin.site.register(Package)
admin.site.register(Release)
admin.site.register(Classifier)
admin.site.register(Distribution)
admin.site.register(Review)
if getattr(settings, 'DJANGOPYPI_MIRRORING', False):
    admin.site.register(MasterIndex)
    admin.site.register(MirrorLog)