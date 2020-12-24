# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/spielmann/prog/bitchest/server/env/src/django-sparkle/sparkle/urls.py
# Compiled at: 2013-07-23 02:22:04
from django.conf.urls.defaults import *
urlpatterns = patterns('sparkle.views', url('^(?P<application_slug>[\\w-]+)/appcast.xml$', 'appcast', name='sparkle_application_appcast'))