# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/admin.py
# Compiled at: 2016-04-16 22:35:57
from django.contrib import admin
from trusts.models import Trust, Role, RolePermission, TrustUserPermission
admin.site.register(Trust, admin.ModelAdmin)
admin.site.register(Role, admin.ModelAdmin)
admin.site.register(RolePermission, admin.ModelAdmin)
admin.site.register(TrustUserPermission, admin.ModelAdmin)