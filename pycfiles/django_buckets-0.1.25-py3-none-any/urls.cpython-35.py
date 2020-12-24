# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/urls.py
# Compiled at: 2017-01-02 04:04:27
# Size of source mod 2**32: 148 bytes
from django.conf.urls import url
from buckets import views
urlpatterns = [
 url('^s3/signed-url/$', views.signed_url, name='s3_signed_url')]