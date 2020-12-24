# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/tests/test_api1/api_urls.py
# Compiled at: 2014-12-31 04:01:41
from django.conf.urls import patterns, url, include
from .. import views
urlpatterns = patterns('', url('^hello', views.blank, name='index'))