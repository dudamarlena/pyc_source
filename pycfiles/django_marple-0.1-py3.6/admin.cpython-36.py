# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marple/admin.py
# Compiled at: 2018-06-30 08:55:37
# Size of source mod 2**32: 196 bytes
from django.contrib import admin
from .models import MarpleItem

class MarpleItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


admin.site.register(MarpleItem, MarpleItemAdmin)