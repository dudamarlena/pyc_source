# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/userprofile/backends/simple/urls.py
# Compiled at: 2012-05-29 05:24:39
from django.conf.urls.defaults import *
from registration.views import activate
from registration.views import register
urlpatterns = patterns('', url('^register/$', register, {'backend': 'userprofile.backends.simple.SimpleBackend'}, name='registration_register'))