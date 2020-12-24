# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jakeurban/Documents/workspace/stellar/django-polaris/polaris/polaris/locale/urls.py
# Compiled at: 2020-01-21 18:42:08
# Size of source mod 2**32: 204 bytes
"""This module defines the URL patterns for the `/language` endpoint."""
from django.urls import path
from polaris.locale.views import language
urlpatterns = [
 path('', language, name='language')]