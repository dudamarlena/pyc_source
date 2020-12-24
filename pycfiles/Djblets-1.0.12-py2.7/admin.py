# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/siteconfig/admin.py
# Compiled at: 2019-06-12 01:17:17
"""Administration UI registrations for site configurations."""
from __future__ import unicode_literals
from django.contrib import admin
from djblets.siteconfig.models import SiteConfiguration

class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site', 'version')


admin.site.register(SiteConfiguration, SiteConfigurationAdmin)