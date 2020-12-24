# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/interim_cms/urls.py
# Compiled at: 2015-06-10 02:57:48
from django.conf.urls import patterns, url
from interim_cms.views import ExampleTileView
urlpatterns = patterns('', url('^example-tile/$', ExampleTileView.as_view(), name='example-tile'))