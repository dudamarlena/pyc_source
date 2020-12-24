# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/src/django_fab_templates/templates/vagrant_project/+project+/urls.py
# Compiled at: 2011-05-20 17:12:49
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os.path
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^(?P<path>favicon\\.ico)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), url('^(?P<path>robots\\.txt)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), url('^(?P<path>[^/]*\\.png)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), url('^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'css')}), url('^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'js')}), url('^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_ROOT}), url('^admin/', include(admin.site.urls)), url('^$', 'views.home', name='home'))