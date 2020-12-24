# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/arpamynt/mezzanine_faq/admin.py
# Compiled at: 2016-01-12 17:48:39
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from .models import FaqPage, FaqQuestion

class FaqQuestionInline(TabularDynamicInlineAdmin):
    model = FaqQuestion


class FaqPageAdmin(PageAdmin):
    inlines = (
     FaqQuestionInline,)


admin.site.register(FaqPage, FaqPageAdmin)