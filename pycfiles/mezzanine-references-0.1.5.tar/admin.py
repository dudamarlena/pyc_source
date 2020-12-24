# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/macht/mezzanine_references/admin.py
# Compiled at: 2015-05-26 09:52:35
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from .models import References, Reference

class ReferenceInline(TabularDynamicInlineAdmin):
    model = Reference


class ReferencesAdmin(PageAdmin):
    inlines = (
     ReferenceInline,)


admin.site.register(References, ReferencesAdmin)