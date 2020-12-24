# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/start/urls.py
# Compiled at: 2020-05-05 16:46:10
# Size of source mod 2**32: 129 bytes
from django.urls import path
from . import views
app_name = 'start'
urlpatterns = [
 path('', (views.start), name='start')]