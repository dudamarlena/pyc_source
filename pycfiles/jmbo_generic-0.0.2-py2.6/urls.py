# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/generic/urls.py
# Compiled at: 2011-09-27 09:30:07
from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from generic.forms import LoginForm
from generic.views import CategoryObjectDetailView, CategoryObjectListView
urlpatterns = patterns('', url('^$', TemplateView.as_view(template_name='generic/home.html'), name='home'), url('^category/(?P<category_slug>[\\w-]+)/$', CategoryObjectListView.as_view(), name='category_object_list'), url('^category/(?P<category_slug>[\\w-]+)/(?P<slug>[\\w-]+)/$', CategoryObjectDetailView.as_view(), name='category_object_detail'), url('^join/$', 'generic.views.join', {}, name='join'), url('^login/$', login, {'authentication_form': LoginForm}, name='login'), url('^logout/$', logout, {}, name='logout'), (
 '^auth/', include('django.contrib.auth.urls')))