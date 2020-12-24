# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mjg/git/django/psu/psu-infotext/psu_infotext/urls.py
# Compiled at: 2019-07-29 18:37:11
# Size of source mod 2**32: 183 bytes
from django.urls import path
from . import views
urlpatterns = [
 path('', (views.index), name='index'),
 path('update', (views.update), name='update')]