# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/urls.py
# Compiled at: 2020-05-04 20:02:30
# Size of source mod 2**32: 161 bytes
from django.urls import path
from cryptapi import views
app_name = 'cryptapi'
urlpatterns = [
 path('callback/', (views.callback), name='callback')]