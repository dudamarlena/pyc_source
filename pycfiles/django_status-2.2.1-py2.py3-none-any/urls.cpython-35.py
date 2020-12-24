# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/perdy/Development/django-status/status/urls.py
# Compiled at: 2016-09-28 11:10:15
# Size of source mod 2**32: 446 bytes
"""
URLs.
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView
app_name = 'status'
urlpatterns = [
 url('^api/', include('status.api.urls')),
 url('^$', TemplateView.as_view(template_name='status/main.html')),
 url('^stats/?$', TemplateView.as_view(template_name='status/stats.html')),
 url('^health/?$', TemplateView.as_view(template_name='status/health.html'))]