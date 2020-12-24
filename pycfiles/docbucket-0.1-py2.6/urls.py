# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/docbucket/urls.py
# Compiled at: 2010-12-14 14:40:32
from django.conf.urls.defaults import *
urlpatterns = patterns('', url('^$', 'docbucket.views.home', name='home'), url('^create/$', 'docbucket.views.create', name='create'), url('^list/$', 'docbucket.views.list', name='list'), url('^list/(?P<doc_class>.+)/$', 'docbucket.views.list', name='list'), url('^manage/$', 'docbucket.views.manage', name='manage'), url('^show/(?P<doc_id>[a-f0-d]{24})/$', 'docbucket.views.show', name='show'), url('^download/(?P<doc_id>[a-f0-d]{24})/$', 'docbucket.views.download', name='download'), url('^search/$', 'docbucket.views.search', name='search'), url('^thumb/(?P<doc_id>[a-f0-d]{24})/(?P<size>.+)/$', 'docbucket.views.document_thumb', name='document_thumb'), url('^thumb/(?P<filename>.+)/$', 'docbucket.views.thumb', name='thumb'))