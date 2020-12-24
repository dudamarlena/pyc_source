# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_signature/urls.py
# Compiled at: 2015-04-30 01:17:41
# Size of source mod 2**32: 207 bytes
from django.conf.urls import patterns, url
from .views import *
urlpatterns = patterns('', url('^sites/', SiteList.as_view()), url('^signature/', SignatureList.as_view()))