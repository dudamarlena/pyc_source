# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/ui/open311_demo/urls.py
# Compiled at: 2014-03-25 14:28:15
from django.conf.urls import patterns, url
urlpatterns = patterns('nodeshot.ui.open311_demo.views', url('^$', 'open311', name='open311'))