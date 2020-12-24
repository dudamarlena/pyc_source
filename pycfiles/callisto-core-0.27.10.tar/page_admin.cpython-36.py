# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/admin/page_admin.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 201 bytes
from django.contrib import admin
from .inlines import QuestionInline

class PageAdmin(admin.ModelAdmin):
    fieldsets = (
     (
      None, {'fields': ('position', 'section')}),)
    inlines = [QuestionInline]