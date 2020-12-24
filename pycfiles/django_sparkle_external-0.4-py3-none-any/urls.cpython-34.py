# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/urls.py
# Compiled at: 2014-07-01 07:17:15
# Size of source mod 2**32: 341 bytes
from django.conf.urls import patterns, url
from .views import channel
urlpatterns = patterns('', url('^(?P<app_slug>[\\w-]+)/appcast\\.xml$', channel, name='sparkle_application_default_channel'), url('^(?P<app_slug>[\\w-]+)/(?P<channel_slug>[\\w-]+)/appcast\\.xml$', channel, name='sparkle_application_channel'))