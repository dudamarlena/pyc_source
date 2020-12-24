# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/himanshubansal/Desktop/meta_management/meta_fields/admin.py
# Compiled at: 2017-02-23 08:49:33
from django.contrib import admin
from meta_fields.models import MetaImage, SiteInformation, OpenGraph, GoogleVerification, BingVerification, BasicTags, AdvancedTags
admin.site.register(MetaImage)
admin.site.register(SiteInformation)
admin.site.register(OpenGraph)
admin.site.register(GoogleVerification)
admin.site.register(BingVerification)
admin.site.register(BasicTags)
admin.site.register(AdvancedTags)