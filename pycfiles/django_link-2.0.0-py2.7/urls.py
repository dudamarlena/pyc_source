# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/link/urls.py
# Compiled at: 2018-05-10 08:40:57
from django.conf.urls import url
from link.views import LinkDetailView, LinkListView
app_name = 'link'
urlpatterns = [
 url('^$', LinkListView.as_view(), name='link-list'),
 url('^(?P<slug>[-\\w]+)/$', LinkDetailView.as_view(), name='link-detail')]