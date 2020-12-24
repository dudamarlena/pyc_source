# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/start/urls.py
# Compiled at: 2020-05-05 16:46:10
# Size of source mod 2**32: 129 bytes
from django.urls import path
from . import views
app_name = 'start'
urlpatterns = [
 path('', (views.start), name='start')]