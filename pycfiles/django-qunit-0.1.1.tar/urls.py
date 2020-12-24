# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/csoyland/src/django-qunit/example/urls.py
# Compiled at: 2010-04-01 01:34:20
from django.conf.urls.defaults import *
urlpatterns = patterns('', url('^qunit/', include('django_qunit.urls')))