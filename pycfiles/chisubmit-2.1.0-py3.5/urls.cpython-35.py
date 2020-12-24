# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/urls.py
# Compiled at: 2018-09-19 12:39:14
# Size of source mod 2**32: 186 bytes
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
 url('^', include('chisubmit.backend.api.urls')),
 url('^admin/', admin.site.urls)]