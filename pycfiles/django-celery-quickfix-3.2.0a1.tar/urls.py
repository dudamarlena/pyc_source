# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bharadwaj/Desktop/django-celery/tests/urls.py
# Compiled at: 2016-04-14 06:46:44
try:
    from django.conf.urls import patterns, include, url, handler500, handler404
except ImportError:
    from django.conf.urls.defaults import patterns, include, url, handler500, handler404

from djcelery.views import apply
urlpatterns = patterns('', url('^apply/(?P<task_name>.+?)/', apply, name='celery-apply'), url('^celery/', include('djcelery.urls')))