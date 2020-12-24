# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/admin.py
# Compiled at: 2010-03-20 20:08:48
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from skins.models import Skin

class skin_inline(admin.TabularInline):
    model = Skin
    extra = 1


admin.site.unregister(Site)
SiteAdmin.inlines = [skin_inline]
admin.site.register(Site, SiteAdmin)