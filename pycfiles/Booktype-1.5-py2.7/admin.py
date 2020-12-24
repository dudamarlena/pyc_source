# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/messaging/admin.py
# Compiled at: 2012-02-14 23:34:00
from booki.messaging import models
from django.contrib import admin
admin.site.register(models.Post)
admin.site.register(models.PostAppearance)
admin.site.register(models.Endpoint)
admin.site.register(models.EndpointConfig)
admin.site.register(models.Following)