# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/urls.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 252 bytes
"""
URL Configuration
https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf.urls import url
from .views import get_table_choices
urlpatterns = [
 url('^cms-qe/table/data', get_table_choices, name='get_table_choices')]