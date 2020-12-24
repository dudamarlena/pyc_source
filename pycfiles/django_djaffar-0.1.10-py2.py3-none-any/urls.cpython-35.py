# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arnaudrenaud/django-djaffar/djaffar/urls.py
# Compiled at: 2016-12-26 05:39:15
# Size of source mod 2**32: 128 bytes
from django.conf.urls import url
from .views import LogActivity
urlpatterns = [
 url('^logs/$', LogActivity.as_view())]