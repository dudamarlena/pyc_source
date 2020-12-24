# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/router/urls.py
# Compiled at: 2016-09-08 07:06:05
# Size of source mod 2**32: 260 bytes
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^$', views.pageView, kwargs={'slug': None, 'homepage': True}),
 url('^(?P<slug>[0-9a-z\\-_]+)/$', views.pageView),
 url('^(?P<path>[0-9a-z\\-_/]+)/$', views.contentView)]