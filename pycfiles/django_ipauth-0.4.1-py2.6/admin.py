# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/ipauth/admin.py
# Compiled at: 2011-06-15 19:10:57
from django.contrib import admin
from ipauth.models import Range

class RangeAuth(admin.ModelAdmin):
    list_display = ('user', 'lower', 'upper')
    search_fields = ('user__first_name', 'user__last_name', 'lower', 'upper')


admin.site.register(Range, RangeAuth)