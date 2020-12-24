# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/forms/urls.py
# Compiled at: 2010-02-24 10:29:35
from django.conf.urls.defaults import *
from django.conf import settings
from softwarefabrica.django.forms.views import ajax_cascade_select
urlpatterns = patterns('', url('^ajax_cascade_select/$', ajax_cascade_select, name='forms-ajax-cascade-select'))