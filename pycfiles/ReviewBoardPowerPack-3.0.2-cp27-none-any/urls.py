# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/urls.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.conf.urls import url
from rbpowerpack.reports import views
urlpatterns = [
 url(b'^$', views.report_list, name=b'powerpack-reports-report-list'),
 url(b'^(?P<report_id>[a-z\\-]+)/$', views.report, name=b'powerpack-reports-report'),
 url(b'^(?P<report_id>[a-z\\-]+)/data/$', views.report_data, name=b'powerpack-reports-report-data'),
 url(b'^queries/users/$', views.query_users, name=b'powerpack-reports-query-users')]