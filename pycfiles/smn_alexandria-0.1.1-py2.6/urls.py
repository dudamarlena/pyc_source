# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/sessions/db/urls.py
# Compiled at: 2010-08-10 05:14:18
from django.conf.urls.defaults import *
from django.conf import settings
from alexandria.sessions.db import views
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', (
 '^stats/static/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, 'static'), (
 '^stats/admin/', include(admin.site.urls)), (
 '^stats/data.js', views.json), (
 '^stats/$', views.home))