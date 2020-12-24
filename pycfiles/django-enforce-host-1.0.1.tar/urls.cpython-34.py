# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jamie/code/django-simple-robots/simple_robots/tests/urls.py
# Compiled at: 2017-10-09 11:54:48
# Size of source mod 2**32: 136 bytes
from django.conf.urls import url
from simple_robots.views import serve_robots
urlpatterns = [
 url('robots.txt', serve_robots)]