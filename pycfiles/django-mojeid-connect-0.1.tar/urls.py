# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/Git/django-mojeid-connect/django_mojeid_connect/urls.py
# Compiled at: 2018-07-09 07:54:10
"""Urls for django_mojeid_connect."""
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django_mojeid_connect.views import CreateUser
urlpatterns = [
 url(b'^$', TemplateView.as_view(template_name=b'homepage.html'), name=b'homepage'),
 url(b'^failed_login/$', TemplateView.as_view(template_name=b'login_fail.html'), name=b'fail_login'),
 url(b'^result/$', TemplateView.as_view(template_name=b'login_results.html'), name=b'login_result'),
 url(b'^create_user/$', CreateUser.as_view(), name=b'create_user'),
 url(b'^oidc/', include(b'mozilla_django_oidc.urls'))]