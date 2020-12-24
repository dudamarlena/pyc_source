# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/Git/django-mojeid-connect/django_mojeid_connect/urls.py
# Compiled at: 2018-07-09 07:54:10
# Size of source mod 2**32: 710 bytes
"""Urls for django_mojeid_connect."""
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django_mojeid_connect.views import CreateUser
urlpatterns = [
 url('^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
 url('^failed_login/$', TemplateView.as_view(template_name='login_fail.html'), name='fail_login'),
 url('^result/$', TemplateView.as_view(template_name='login_results.html'), name='login_result'),
 url('^create_user/$', CreateUser.as_view(), name='create_user'),
 url('^oidc/', include('mozilla_django_oidc.urls'))]