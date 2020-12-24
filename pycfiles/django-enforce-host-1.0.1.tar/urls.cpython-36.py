# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jamie/code/django-enforce-hostname/enforce_hostname/tests/urls.py
# Compiled at: 2017-11-24 10:05:22
# Size of source mod 2**32: 147 bytes
from django.conf.urls import url
from django.http import HttpResponse
urlpatterns = [
 url('^$', lambda request: HttpResponse('success'))]