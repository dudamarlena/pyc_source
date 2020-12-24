# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/admin.py
# Compiled at: 2016-09-19 07:37:17
from __future__ import unicode_literals
from django.contrib import admin
from . import models

class AuthResultAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'state', 'user', 'modified')
    ordering = ('modified', )
    list_filter = ('state', 'user')


admin.site.register(models.AuthResult, AuthResultAdmin)