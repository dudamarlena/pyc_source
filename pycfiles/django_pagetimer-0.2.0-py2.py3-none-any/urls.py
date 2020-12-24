# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-pagetimer/pagetimer/urls.py
# Compiled at: 2016-05-11 11:03:27
from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
import pagetimer.views as views
urlpatterns = [
 url('^$', user_passes_test(lambda x: x.is_superuser)(views.DashboardView.as_view(paginate_by=100)), name='pagetimer-dashboard'),
 url('^filter/$', user_passes_test(lambda x: x.is_superuser)(views.FilterView.as_view(paginate_by=100)), name='pagetimer-filter'),
 url('^csv/$', user_passes_test(lambda x: x.is_superuser)(views.CSVView.as_view()), name='pagetimer-csv'),
 url('^purge/$', user_passes_test(lambda x: x.is_superuser)(views.PurgeView.as_view()), name='pagetimer-purge'),
 url('^endpoint/$', views.PageTimerEndpointView.as_view(), name='pagetimer-endpoint')]