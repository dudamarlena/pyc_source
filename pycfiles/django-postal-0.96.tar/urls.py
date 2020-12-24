# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mick/src/django-postal/src/postal/urls.py
# Compiled at: 2014-06-03 14:03:01
from django.conf.urls import *
urlpatterns = patterns('', (
 '^api/', include('postal.api.urls')), url('^update_postal_address/$', 'postal.views.changed_country', name='changed_country'))