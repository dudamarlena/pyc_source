# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rohan/Django/django-admin-kit/.venv/lib/python3.6/site-packages/tests/urls.py
# Compiled at: 2017-12-04 09:10:50
# Size of source mod 2**32: 318 bytes
from django.conf.urls import url, include
from django.contrib import admin
import admin_kit, nested_admin
urlpatterns = [
 url('admin/', (admin.site.urls), name='admin'),
 url('nested_admin/', (include('nested_admin.urls')), name='nested_admin'),
 url('admin_kit/', (admin_kit.site.urls), name='admin_kit')]