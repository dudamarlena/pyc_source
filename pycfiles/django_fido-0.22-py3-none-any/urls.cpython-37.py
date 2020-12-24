# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/urls.py
# Compiled at: 2020-02-19 07:40:53
# Size of source mod 2**32: 1008 bytes
"""URLs for django_fido application."""
from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from .views import Fido2AuthenticationRequestView, Fido2AuthenticationView, Fido2RegistrationRequestView, Fido2RegistrationView
app_name = 'django_fido'
urlpatterns = [
 url('^registration/$', (Fido2RegistrationView.as_view()), name='registration'),
 url('^registration/request/$', (Fido2RegistrationRequestView.as_view()), name='registration_request'),
 url('^registration/done/$', TemplateView.as_view(template_name='django_fido/registration_done.html'), name='registration_done'),
 url('^authentication/$', (Fido2AuthenticationView.as_view()), name='authentication'),
 url('^authentication/request/$', (Fido2AuthenticationRequestView.as_view()), name='authentication_request'),
 url('^jsi18n/$', (JavaScriptCatalog.as_view()), name='javascript_catalog')]