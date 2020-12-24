# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/django_project_templates/templates/newsapps_project/+project+/configs/common/urls.py
# Compiled at: 2010-03-28 09:05:20
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', (
 '^admin/doc/', include('django.contrib.admindocs.urls')), (
 '^admin/(.*)', admin.site.root), (
 '^site_media/(?P<path>.*)$', 'django.views.static.serve',
 {'document_root': settings.MEDIA_ROOT}))