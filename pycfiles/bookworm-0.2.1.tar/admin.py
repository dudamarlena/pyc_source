# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/messaging/admin.py
# Compiled at: 2012-02-14 23:34:00
from booki.messaging import models
from django.contrib import admin
admin.site.register(models.Post)
admin.site.register(models.PostAppearance)
admin.site.register(models.Endpoint)
admin.site.register(models.EndpointConfig)
admin.site.register(models.Following)