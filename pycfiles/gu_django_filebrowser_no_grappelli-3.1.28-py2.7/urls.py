# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/urls.py
# Compiled at: 2016-01-24 14:43:49
from django.conf import urls
from filebrowser import views
urlpatterns = [
 urls.url('^browse/$', views.browse, name='fb_browse'),
 urls.url('^mkdir/', views.mkdir, name='fb_mkdir'),
 urls.url('^upload/', views.upload, name='fb_upload'),
 urls.url('^rename/$', views.rename, name='fb_rename'),
 urls.url('^delete/$', views.delete, name='fb_delete'),
 urls.url('^versions/$', views.versions, name='fb_versions'),
 urls.url('^check_file/$', views._check_file, name='fb_check'),
 urls.url('^upload_file/$', views._upload_file, name='fb_do_upload')]