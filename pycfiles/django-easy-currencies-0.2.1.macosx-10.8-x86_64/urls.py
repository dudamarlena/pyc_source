# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/urls.py
# Compiled at: 2014-10-16 04:19:59
from __future__ import unicode_literals
from django_easy_currencies.views.ChangeCurrencyView import ChangeCurrencyView
from django.conf.urls import patterns, url
urlpatterns = patterns(b'', url(regex=b'^change/$', view=ChangeCurrencyView.as_view(), name=b'change_currency'))