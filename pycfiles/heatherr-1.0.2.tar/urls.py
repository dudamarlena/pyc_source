# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/smn/heatherr/heatherr/urls.py
# Compiled at: 2016-01-28 05:47:10
"""heatherr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from heatherr import dispatcher
urlpatterns = [
 url('^$', RedirectView.as_view(url=settings.LOGIN_URL)),
 url('^', include('social.apps.django_app.urls', namespace='social')),
 url('^commands/', dispatcher.view, name='dispatcher'),
 url('^announce/', dispatcher.view, name='dispatcher'),
 url('^accounts/', include('heatherr.account.urls', namespace='accounts')),
 url('^admin/', include(admin.site.urls))]