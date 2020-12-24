# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/urls.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 213 bytes
from django.conf.urls import url
from . import views
app_name = 'djconnectwise'
urlpatterns = [
 url(regex='^callback/$',
   view=(views.CallBackView.as_view()),
   name='callback')]