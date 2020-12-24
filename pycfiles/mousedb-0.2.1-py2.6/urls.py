# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/urls.py
# Compiled at: 2010-06-20 21:03:38
"""Generic base url directives.

These directives will redirect requests to app specific pages, and provide redundancy in possible names."""
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', (
 '^ajax_select/', include('ajax_select.urls')), (
 '^admin/doc/', include('django.contrib.admindocs.urls')), (
 '^admin/', include(admin.site.urls)), url('^accounts/login/', 'django.contrib.auth.views.login', name='login'), url('^mouse/', include('mousedb.animal.urls.mouse')), url('^mice/', include('mousedb.animal.urls.mouse')), url('^animals?/', include('mousedb.animal.urls.mouse')), url('^strains?/', include('mousedb.animal.urls.strain')), url('^dates?/', include('mousedb.animal.urls.date')), url('^breedings?/', include('mousedb.animal.urls.breeding')), url('^breeding_cages?/', include('mousedb.animal.urls.breeding')), url('^todo/', include('mousedb.animal.urls.todo')), url('^cages?/', include('mousedb.animal.urls.cage')), url('^experiments?/', include('mousedb.data.urls.experiment')), url('^study/', include('mousedb.data.urls.study')), url('^studies/', include('mousedb.data.urls.study')), url('^treatments?/', include('mousedb.data.urls.treatment')), url('^parameters?/', include('mousedb.data.urls.parameter')), url('^plugs?/', include('mousedb.timed_mating.urls')), url('^plugevents?/', include('mousedb.timed_mating.urls')), url('^plug_events?/', include('mousedb.timed_mating.urls')), url('^timedmatings?/', include('mousedb.timed_mating.urls')), url('^timed_matings?/', include('mousedb.timed_mating.urls')), url('^specs?/$', 'django.views.generic.simple.direct_to_template', {'template': 'specs.html'}, name='specs'), url('^index/$', 'mousedb.views.home', name='home'), url('^/?$', 'mousedb.views.home'))