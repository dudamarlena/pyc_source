# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/urls.py
# Compiled at: 2018-04-26 06:52:12
# Size of source mod 2**32: 315 bytes
from __future__ import unicode_literals
from django.conf.urls import url
from . import views
app_name = 'robokassa'
urlpatterns = [
 url('^result/$', views.receive_result, name='result'),
 url('^success/$', views.success, name='success'),
 url('^fail/$', views.fail, name='fail')]