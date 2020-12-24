# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/urls.py
# Compiled at: 2014-12-08 04:48:44
from django.conf.urls import patterns, url
from djinn_contenttypes.views.share import ShareView, ShareActivityView
urlpatterns = patterns('', url('^content/share/(?P<ctype>[\\w]+)/(?P<id>[\\d]+)/?$', ShareView.as_view(), name='djinn_contenttypes_share'), url('^content/share/(?P<activity_id>[\\d]+)/?$', ShareActivityView.as_view(), name='djinn_contenttypes_share'))