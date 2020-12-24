# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/star/admin.py
# Compiled at: 2011-10-07 22:01:57
from django.contrib import admin
from models import Star

class StarAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'author', 'comment')
    search_fields = ('content_object', )
    filter_fields = ('author', )


admin.site.register(Star, StarAdmin)