# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/urls.py
# Compiled at: 2018-08-14 12:18:01
# Size of source mod 2**32: 451 bytes
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
 url('^/', include('dash_test_runner.testapp.urls')),
 url('^manage/', include('dash.orgs.urls')),
 url('^manage/', include('dash.stories.urls')),
 url('^manage/', include('dash.dashblocks.urls')),
 url('^manage/', include('dash.categories.urls')),
 url('^users/', include('dash.users.urls')),
 url('^admin/', admin.site.urls)]