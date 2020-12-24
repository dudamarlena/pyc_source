# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zenobius/Dev/django-apps/django-ikari/ikari/error_urls.py
# Compiled at: 2013-06-26 17:21:56
from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse, reverse_lazy
from . import views
from . import settings
urlpatterns = patterns('', url('^error/domain/inactive/$', views.DomainErrorView.as_view(), settings.ERRORCONTEXT_INACTIVE, name='domains-inactive'), url('^error/domain/invalid/$', views.DomainErrorView.as_view(), settings.ERRORCONTEXT_INVALID, name='domains-unavailable'), url('^error/domain/private/$', views.DomainErrorView.as_view(), settings.ERRORCONTEXT_PRIVATE, name='domains-not-public'))