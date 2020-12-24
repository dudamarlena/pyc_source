# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/user/urls.py
# Compiled at: 2015-01-18 07:28:37
from django.conf.urls import patterns, url
from . import views
from django.views.generic import TemplateView
urlpatterns = patterns('', url('^login$', views.login, name='login'), url('^logout$', views.logout, {'next_page': '/'}, name='logout'), url('^profile$', TemplateView.as_view(template_name='glue/home.html'), name='profile'))