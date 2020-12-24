# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/urls.py
# Compiled at: 2015-04-06 03:47:41
""" URL specification for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from ninecms import views
urlpatterns = patterns('', url('^cms/content/$', login_required(views.ContentView.as_view()), name='content'), url('^cms/$', RedirectView.as_view(pattern_name='ninecms:content', permanent=True)), url('^cms/content/(?P<node_id>\\d+)/$', views.ContentNodeView.as_view(), name='content_node'), url('^cms/content/add/$', login_required(views.ContentNodeAddView.as_view()), name='content_node_add'), url('^cms/content/(?P<node_id>\\d+)/edit/$', login_required(views.ContentNodeEditView.as_view()), name='content_node_edit'), url('^contact/form/$', views.ContactView.as_view(), name='contact'), url('^(?P<url_alias>[/\\w\\-_]+)$', views.AliasView.as_view(), name='alias'), url('^$', views.IndexView.as_view(), name='index'))