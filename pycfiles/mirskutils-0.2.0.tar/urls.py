# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./webapp/urls.py
# Compiled at: 2014-06-01 18:18:49
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
import core.views
if settings.DEBUGGER:
    import wingdbstub
urlpatterns = patterns('', url('^', include('webapp.registration.urls')), url('^', include('django.contrib.auth.urls')), url('^admin/', include(admin.site.urls)))
if settings.DEBUG:
    urlpatterns = patterns('', url('^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}), url('', include('django.contrib.staticfiles.urls'))) + urlpatterns