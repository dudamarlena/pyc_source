# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/media/urls/photos.py
# Compiled at: 2012-04-05 17:42:51
from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from media.models import Photo, PhotoSet
urlpatterns = patterns('', url('^$', view=ListView.as_view(model=Photo), name='photo_list'), url('^(?P<slug>[-\\w]+)/$', view=DetailView.as_view(model=Photo), name='photo_detail'), url('^sets/$', view=ListView.as_view(model=PhotoSet), name='photo_set_list'), url('^sets/(?P<slug>[-\\w]+)/$', view=DetailView.as_view(model=PhotoSet), name='photo_set_detail'))