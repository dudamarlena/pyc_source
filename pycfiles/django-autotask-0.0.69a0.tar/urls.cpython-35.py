# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/urls.py
# Compiled at: 2019-11-01 16:37:20
# Size of source mod 2**32: 219 bytes
from django.conf.urls import url
from djautotask import views
app_name = 'djautotask'
urlpatterns = [
 url(regex='^callback/$', view=views.CallBackView.as_view(), name='callback')]