# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/urls.py
# Compiled at: 2017-05-03 05:57:29
from django.conf.urls import include, url
from jmbo.views import ObjectDetail, ObjectList, image_scale_url
urlpatterns = [
 url('^detail/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='modelbase-detail'),
 url('^detail/(?P<category_slug>[\\w-]+)/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='modelbase-categorized-detail'),
 url('^list/(?P<app_label>[\\w-]+)/(?P<model>[\\w-]+)/$', ObjectList.as_view(), name='modelbase-list'),
 url('^image-scale-url/(?P<pk>[\\w-]+)/(?P<size>[\\w-]+)/$', image_scale_url, name='image-scale-url')]