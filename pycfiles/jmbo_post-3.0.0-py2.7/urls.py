# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/post/urls.py
# Compiled at: 2017-07-03 11:37:50
from django.conf.urls import include, url
from jmbo.views import ObjectDetail
urlpatterns = [
 url('^(?P<category_slug>[\\w-]+)/(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='post-categorized-detail'),
 url('^(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='post-detail')]