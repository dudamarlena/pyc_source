# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/rabelvideo/ninecms/urls.py
# Compiled at: 2015-11-13 10:58:52
# Size of source mod 2**32: 1555 bytes
""" URL specification for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import RedirectView
from ninecms import views
urlpatterns = [
 url('^cms/$', RedirectView.as_view(pattern_name='admin:index', permanent=True)),
 url('^cms/content/$', RedirectView.as_view(pattern_name='admin:ninecms_node_changelist', permanent=True)),
 url('^cms/content/(?P<node_id>\\d+)/$', views.ContentNodeView.as_view(), name='content_node'),
 url('^cms/status/$', staff_member_required(views.StatusView.as_view()), name='status'),
 url('^contact/form/$', views.ContactView.as_view(), name='contact'),
 url('^user/login/$', views.LoginView.as_view(), name='login'),
 url('^user/logout/$', login_required(views.LogoutView.as_view()), name='logout'),
 url('^(?P<url_alias>[/\\w\\-_]+)$', views.AliasView.as_view(), name='alias'),
 url('^$', views.IndexView.as_view(), name='index')]