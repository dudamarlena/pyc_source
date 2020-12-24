# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/core/admin.py
# Compiled at: 2018-11-08 07:12:47
# Size of source mod 2**32: 204 bytes
from django.contrib import admin
from . import models

@admin.register(models.ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'service')
    list_filter = ('owner', 'service')