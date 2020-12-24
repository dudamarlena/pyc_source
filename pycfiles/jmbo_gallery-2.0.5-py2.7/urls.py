# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gallery/urls.py
# Compiled at: 2016-03-08 06:27:04
from django.conf.urls import patterns, url
from jmbo.views import ObjectDetail
urlpatterns = patterns('', url('^(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='gallery_object_detail'), url('^video/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='videoembed_object_detail'), url('^image/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='galleryimage_object_detail'))