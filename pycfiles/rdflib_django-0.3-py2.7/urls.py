# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/urls.py
# Compiled at: 2012-10-06 02:34:18
"""
The application provides no URLs of its own.
In development mode, this will include the admin package.
"""
from django.conf import settings
from django.conf.urls import patterns, include
if hasattr(settings, 'DJANGO_RDFLIB_DEVELOP') and getattr(settings, 'DJANGO_RDFLIB_DEVELOP'):
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = patterns('', (
     '^admin/doc/', include('django.contrib.admindocs.urls')), (
     '^admin/', include(admin.site.urls)))