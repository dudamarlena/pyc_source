# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arnaudrenaud/django-djaffar/djaffar/urls.py
# Compiled at: 2017-01-04 05:55:20
# Size of source mod 2**32: 157 bytes
from django.conf.urls import url
from .views import ActivityDetail
urlpatterns = [
 url('^log/$', (ActivityDetail.as_view()), name='activity_detail')]