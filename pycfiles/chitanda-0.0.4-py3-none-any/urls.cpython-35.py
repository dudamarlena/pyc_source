# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/urls.py
# Compiled at: 2018-09-19 12:39:14
# Size of source mod 2**32: 186 bytes
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
 url('^', include('chisubmit.backend.api.urls')),
 url('^admin/', admin.site.urls)]