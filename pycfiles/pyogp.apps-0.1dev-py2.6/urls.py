# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/web/django/pyogp_webbot/urls.py
# Compiled at: 2009-12-22 03:50:08
from django.conf.urls.defaults import *
urlpatterns = patterns('', ('^$', 'pyogp_webbot.login.views.index'), ('^pyogp_webbot/$',
                                                                      'pyogp_webbot.login.views.index'), ('^pyogp_webbot/login/$',
                                                                                                          'pyogp_webbot.login.views.login'), ('^pyogp_webbot/login/login_request/$',
                                                                                                                                              'pyogp_webbot.login.views.login_request'))