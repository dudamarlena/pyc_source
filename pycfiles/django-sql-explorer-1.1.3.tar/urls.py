# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/urls.py
# Compiled at: 2019-07-02 17:20:17
from django.conf.urls import url
from explorer.views import QueryView, CreateQueryView, PlayQueryView, DeleteQueryView, ListQueryView, ListQueryLogView, DownloadFromSqlView, DownloadQueryView, StreamQueryView, EmailCsvQueryView, SchemaView, format_sql
urlpatterns = [
 url('(?P<query_id>\\d+)/$', QueryView.as_view(), name='query_detail'),
 url('(?P<query_id>\\d+)/download$', DownloadQueryView.as_view(), name='download_query'),
 url('(?P<query_id>\\d+)/stream$', StreamQueryView.as_view(), name='stream_query'),
 url('download$', DownloadFromSqlView.as_view(), name='download_sql'),
 url('(?P<query_id>\\d+)/email_csv$', EmailCsvQueryView.as_view(), name='email_csv_query'),
 url('(?P<pk>\\d+)/delete$', DeleteQueryView.as_view(), name='query_delete'),
 url('new/$', CreateQueryView.as_view(), name='query_create'),
 url('play/$', PlayQueryView.as_view(), name='explorer_playground'),
 url('schema/(?P<connection>.+)$', SchemaView.as_view(), name='explorer_schema'),
 url('logs/$', ListQueryLogView.as_view(), name='explorer_logs'),
 url('format/$', format_sql, name='format_sql'),
 url('^$', ListQueryView.as_view(), name='explorer_index')]