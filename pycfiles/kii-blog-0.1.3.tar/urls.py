# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/urls.py
# Compiled at: 2014-12-16 11:40:40
from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from . import models, views, forms
from kii.stream import views as stream_views
entry_patterns = patterns('', url('^$', views.EntryList.as_view(), name='list'), url('^create$', stream_views.Create.as_view(form_class=forms.EntryForm), name='create'), url('^(?P<pk>\\d+)/update$', stream_views.Update.as_view(form_class=forms.EntryForm), name='update'), url('^(?P<slug>[\\w-]+)/update$', stream_views.Update.as_view(form_class=forms.EntryForm), name='update'), url('^(?P<slug>[\\w-]+)$', stream_views.Detail.as_view(model=models.Entry), name='detail'))
urlpatterns = patterns('', url('^$', RedirectView.as_view(url=reverse_lazy('kii:blog:entry:list'), permanent=False), name='index'), url('^entries/', include(entry_patterns, namespace='entry', app_name='entry')))