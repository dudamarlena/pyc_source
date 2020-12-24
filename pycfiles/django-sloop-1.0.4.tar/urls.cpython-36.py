# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/urls.py
# Compiled at: 2019-08-14 11:46:19
# Size of source mod 2**32: 200 bytes
from django.conf.urls import url
from .views import CreateDeleteDeviceView
app_name = 'django_sloop'
urlpatterns = (
 url('^$', (CreateDeleteDeviceView.as_view()), name='create-delete-device'),)