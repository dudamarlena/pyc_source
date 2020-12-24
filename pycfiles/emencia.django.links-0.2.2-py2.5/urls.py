# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/links/urls.py
# Compiled at: 2010-01-14 11:17:33
"""Urls for emencia.news"""
from django.conf.urls.defaults import *
from emencia.django.links.views import links_by_language
urlpatterns = patterns('', url('^$', links_by_language, name='links_list'))