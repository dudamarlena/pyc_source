# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmc/projects/django-monkey-team/tests/test_project/urls.py
# Compiled at: 2013-03-07 07:10:24
try:
    from django.conf.urls import patterns, handler404, handler500, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, handler404, handler500, include, url

from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^admin/', include(admin.site.urls)))