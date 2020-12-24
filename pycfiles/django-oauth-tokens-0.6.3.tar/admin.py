# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/admin.py
# Compiled at: 2015-01-25 03:14:29
from django.contrib import admin
from .models import AccessToken, UserCredentials

class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('provider', 'access_token', 'user_credentials', 'granted_at', 'expires_at')
    list_display_links = ('access_token', )
    list_filter = ('provider', )


class UserCredentialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'username', 'active')
    list_filter = ('provider', )


admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(UserCredentials, UserCredentialsAdmin)