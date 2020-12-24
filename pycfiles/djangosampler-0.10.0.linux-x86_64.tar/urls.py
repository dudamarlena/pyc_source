# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/urls.py
# Compiled at: 2015-11-17 05:08:04
from django.conf.urls import patterns, url
import views
urlpatterns = patterns('', url('^queries/(?P<query_type>[\\w ]+)/(?P<date_string>[-\\w\\d]+)/(?P<sort>(-|\\w)+)/(?P<offset>\\d+)/$', views.queries, name='queries'), url('^query/(?P<query_hash>[-0-9]+)/$', views.query, name='query'), url('^$', views.index, name='index'))