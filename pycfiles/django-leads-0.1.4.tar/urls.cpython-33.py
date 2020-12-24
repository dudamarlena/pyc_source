# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dnavarro/repos/django-leads/leads/urls.py
# Compiled at: 2014-02-26 09:41:22
# Size of source mod 2**32: 263 bytes
from django.conf.urls import patterns, url
from .views import IndexView, ThanksView
urlpatterns = patterns('', url('^$', IndexView.as_view(), name='index'), url('^thanks/$', ThanksView.as_view(), name='thanks_register'))