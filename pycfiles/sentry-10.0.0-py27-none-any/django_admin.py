# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/django_admin.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from copy import copy
from django.contrib import admin
from django.conf.urls import include, patterns, url
from sentry.auth.superuser import is_active_superuser

class RestrictiveAdminSite(admin.AdminSite):

    def has_permission(self, request):
        return is_active_superuser(request)


def make_site():
    admin.autodiscover()
    admin.autodiscover = lambda : None
    site = RestrictiveAdminSite()
    site._registry = copy(admin.site._registry)
    admin.site._registry = {}
    admin.site = site
    return site


site = make_site()
urlpatterns = patterns('', url('^admin/', include(site.urls)))