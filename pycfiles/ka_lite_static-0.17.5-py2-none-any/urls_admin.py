# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/tests/urls_admin.py
# Compiled at: 2018-07-11 18:15:30
"""
Test URLs for auth admins.
"""
from django.conf.urls import patterns, include
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.urls import urlpatterns
site = admin.AdminSite(name='auth_test_admin')
site.register(User, UserAdmin)
site.register(Group, GroupAdmin)
urlpatterns = urlpatterns + patterns('', (
 '^admin/', include(site.urls)))