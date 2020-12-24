# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/profile/backends/simple/urls.py
# Compiled at: 2010-08-04 04:05:50
from django.conf.urls.defaults import *
from registration.views import activate
from registration.views import register
urlpatterns = patterns('', url('^register/$', register, {'backend': 'profile.backends.simple.SimpleBackend'}, name='registration_register'))