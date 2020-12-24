# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mjg/git/django/psu/psu-infotext/psu_infotext/urls.py
# Compiled at: 2019-07-29 18:37:11
# Size of source mod 2**32: 183 bytes
from django.urls import path
from . import views
urlpatterns = [
 path('', (views.index), name='index'),
 path('update', (views.update), name='update')]