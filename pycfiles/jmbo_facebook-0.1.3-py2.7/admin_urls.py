# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jmbo_facebook/admin_urls.py
# Compiled at: 2013-05-14 09:27:46
from django.conf.urls.defaults import patterns, url, include
urlpatterns = patterns('', (
 '^admin/jmbo_facebook/handler/$',
 'jmbo_facebook.admin_views.handler', {},
 'jmbo-facebook-handler'))