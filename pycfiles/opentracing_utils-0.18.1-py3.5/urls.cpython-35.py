# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_django/urls.py
# Compiled at: 2019-02-13 08:31:21
# Size of source mod 2**32: 311 bytes
from django.conf.urls import url
import app.views as views
urlpatterns = [
 url('^$', views.home, name='home'),
 url('^user', views.user, name='user'),
 url('^error', views.error, name='error'),
 url('^bad', views.bad_request, name='bad'),
 url('^nested', views.nested, name='nested')]