# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hgwebproxy/admin.py
# Compiled at: 2009-07-25 21:30:12
from django.contrib import admin
from hgwebproxy.models import Repository

class RepositoryAdmin(admin.ModelAdmin):
    list_display = [
     'name', 'owner']
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Repository, RepositoryAdmin)