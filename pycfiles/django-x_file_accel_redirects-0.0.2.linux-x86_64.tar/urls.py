# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/imposeren/kava/42-kavyarnya/.env/lib/python2.7/site-packages/x_file_accel_redirects/urls.py
# Compiled at: 2014-03-28 04:49:45
from django.conf.urls.defaults import patterns, url
from x_file_accel_redirects import views
urlpatterns = patterns('', url('^(?P<prefix>[^/]+)/(?P<filepath>.+)$', views.accel_view, name='accel_view'), url('^(?P<prefix>[^/]+)$', views.accel_view, name='accel_view_root'))