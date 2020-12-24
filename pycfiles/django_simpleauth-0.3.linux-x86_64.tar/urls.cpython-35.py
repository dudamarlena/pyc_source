# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratheek/msc/pythons/lib/python3.5/site-packages/simpleauth/urls.py
# Compiled at: 2017-02-09 05:20:29
# Size of source mod 2**32: 197 bytes
from django.conf.urls import url
from . import views
app_name = 'simpleauth'
urlpatterns = [
 url('^$', views.start, name='start'),
 url('register/$', views.register, name='register')]