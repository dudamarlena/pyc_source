# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insight/urls.py
# Compiled at: 2014-09-10 08:36:20
from django.conf.urls.defaults import patterns, url
from insight.views import set_origin_code
urlpatterns = patterns('', url('^i/(?P<code>[\\w-]+)/$', set_origin_code, name='set-origin-code'))