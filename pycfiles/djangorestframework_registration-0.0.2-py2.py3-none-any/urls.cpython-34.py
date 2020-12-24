# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eugene/Workspace/django-rest-framework-registration/rest_framework_registration/urls.py
# Compiled at: 2016-04-01 13:19:49
# Size of source mod 2**32: 652 bytes
from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
 url('^registrations/$', views.RegistrationView.as_view(), name='registration_register'),
 url('^activations/(?P<activation_key>[-:\\w]+)/$', views.ActivationView.as_view(), name='registration_activate'),
 url('^activation-complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'), name='registration_activation_complete')]
urlpatterns = format_suffix_patterns(urlpatterns)