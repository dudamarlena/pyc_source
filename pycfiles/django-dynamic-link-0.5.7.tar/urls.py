# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-dynamic-link/example/urls.py
# Compiled at: 2012-11-15 17:25:46
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()
from dynamicLink import presettings
urlpatterns = patterns('', (
 '^$', direct_to_template, {'template': 'home.html'}), (
 '^\\w+/%s/' % presettings.DYNAMIC_LINK_URL_BASE_COMPONENT, include('dynamicLink.urls')), (
 '^admin/doc/', include('django.contrib.admindocs.urls')), url('^admin/', include(admin.site.urls)))