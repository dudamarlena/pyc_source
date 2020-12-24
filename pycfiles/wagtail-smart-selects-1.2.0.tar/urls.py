# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rmartins/Desenvolvimento/Django/Apps/wagtaildemo/smart_selects/urls.py
# Compiled at: 2016-01-06 07:19:32
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

urlpatterns = patterns('smart_selects.views', url('^all/(?P<app>[\\w\\-]+)/(?P<model>[\\w\\-]+)/(?P<field>[\\w\\-]+)/(?P<foreign_key_app_name>[\\w\\-]+)/(?P<foreign_key_model_name>[\\w\\-]+)/(?P<foreign_key_field_name>[\\w\\-]+)/(?P<value>[\\w\\-]+)/$', 'filterchain_all', name='chained_filter_all'), url('^filter/(?P<app>[\\w\\-]+)/(?P<model>[\\w\\-]+)/(?P<field>[\\w\\-]+)/(?P<foreign_key_app_name>[\\w\\-]+)/(?P<foreign_key_model_name>[\\w\\-]+)/(?P<foreign_key_field_name>[\\w\\-]+)/(?P<value>[\\w\\-]+)/$', 'filterchain', name='chained_filter'), url('^filter/(?P<app>[\\w\\-]+)/(?P<model>[\\w\\-]+)/(?P<manager>[\\w\\-]+)/(?P<field>[\\w\\-]+)/(?P<foreign_key_app_name>[\\w\\-]+)/(?P<foreign_key_model_name>[\\w\\-]+)/(?P<foreign_key_field_name>[\\w\\-]+)/(?P<value>[\\w\\-]+)/$', 'filterchain', name='chained_filter'))