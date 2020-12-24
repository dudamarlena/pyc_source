# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/test_urls.py
# Compiled at: 2013-08-19 20:37:49
from django.conf.urls import patterns, include, url
urlpatterns = patterns('', url('^chalk/', include('chalk.urls')))