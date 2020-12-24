# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/urls.py
# Compiled at: 2015-03-06 05:08:58
from django.conf.urls import patterns, url, include
from .views import unsubscribe, unsubscribed
app_urlpatterns = patterns('', url('^unsubscribe/(?P<hashed>.*)/(?P<data>.*)/$', unsubscribe, name='unsubscribe'), url('^unsubscribe/complete/$', unsubscribed, name='unsubscribed'))
urlpatterns = patterns('', url('^', include(app_urlpatterns, namespace='mass_post_office')))