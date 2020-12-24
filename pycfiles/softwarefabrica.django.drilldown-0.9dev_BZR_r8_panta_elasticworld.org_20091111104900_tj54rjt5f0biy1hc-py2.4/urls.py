# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/drilldown/urls.py
# Compiled at: 2009-10-22 10:41:45
from django.conf.urls.defaults import *
from django.conf import settings
from softwarefabrica.django.drilldown.views import generic_drilldown
urlpatterns = patterns('', url('^(?P<app_label>[a-zA-Z0-9_\\-\\.]+)/(?P<model_name>[a-zA-Z0-9_]+)/(?P<url>.*)$', generic_drilldown, name='drilldown-generic-drilldown'))