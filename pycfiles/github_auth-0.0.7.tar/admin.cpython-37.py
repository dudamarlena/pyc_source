# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\Desktop\programlarim\djangoapps\github-auth\github_auth\admin.py
# Compiled at: 2019-09-02 16:03:56
# Size of source mod 2**32: 395 bytes
from django.contrib.admin import ModelAdmin, site
from django.http import Http404
from .models import GithubAuthUser

class GithubAuthUserAdmin(ModelAdmin):
    list_display = [
     'user']
    list_display_links = list_display
    search_fields = list_display
    fields = ['user', 'code', 'access_token', 'extra_data']


site.register(GithubAuthUser, GithubAuthUserAdmin)