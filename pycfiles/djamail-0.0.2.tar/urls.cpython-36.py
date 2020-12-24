# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tony/work/buser/djamail/djamail/urls.py
# Compiled at: 2019-10-14 23:34:53
# Size of source mod 2**32: 116 bytes
from django.conf.urls import url
from djamail import views
urlpatterns = [
 url('^preview$', views.preview)]