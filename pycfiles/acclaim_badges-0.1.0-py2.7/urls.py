# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acclaim_badges/urls.py
# Compiled at: 2017-06-02 15:35:20
"""
URLs for acclaim_badges.
"""
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import BadgeCourseList
from .views import BadgeCourseCreate
from .views import BadgeCourseDelete
from .views import BadgeCourseUpdate
from .views import AcclaimTokenList
from .views import AcclaimTokenCreate
from .views import AcclaimTokenDelete
from .views import AcclaimTokenUpdate
urlpatterns = [
 url(b'^tokens/', AcclaimTokenList.as_view(), name=b'acclaim-tokens'),
 url(b'^token/add/$', AcclaimTokenCreate.as_view(), name=b'acclaim-token-add'),
 url(b'^token/update/(?P<pk>[0-9]+)/$', AcclaimTokenUpdate.as_view(), name=b'acclaim-token-update'),
 url(b'^token/delete/(?P<pk>[0-9]+)/$', AcclaimTokenDelete.as_view(), name=b'acclaim-token-delete'),
 url(b'badge-course/add/$', BadgeCourseCreate.as_view(), name=b'badge-course-add'),
 url(b'^badge-courses/$', BadgeCourseList.as_view(), name=b'badge-courses'),
 url(b'^badge-course/delete/(?P<pk>[0-9]+)/$', BadgeCourseDelete.as_view(), name=b'badge-course-delete'),
 url(b'^badge-course/update/(?P<pk>[0-9]+)/$', BadgeCourseUpdate.as_view(), name=b'badge-course-update')]