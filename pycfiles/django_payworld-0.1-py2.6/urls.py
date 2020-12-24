# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_payworld/urls.py
# Compiled at: 2012-02-15 01:02:40
from django.conf.urls.defaults import patterns, include, url
from django_payworld import views
urlpatterns = patterns('', url('^success/$', views.success, name='payworld-success'), url('^failure/$', views.failure, name='payworld-failure'), url('^result/$', views.result, name='payworld-result'))