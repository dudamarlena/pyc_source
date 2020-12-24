# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/baseacct/urls.py
# Compiled at: 2016-05-17 14:52:55
from webutils.baseacct.config import Config
from webutils.baseacct import views
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
config = Config()
urlpatterns = [
 url('^login/$', auth_views.login, {'template_name': 'baseacct/login.html', 
    'authentication_form': config.get_login_form()}, name='baseacct-login'),
 url('^logout/$', auth_views.logout, {'template_name': 'baseacct/logout.html'}, name='baseacct-logout'),
 url('^logout-login/$', auth_views.logout_then_login, {'login_url': config.get_login_url()}, name='baseacct-logout-login'),
 url('^password_change/$', views.password_change, {'template': 'baseacct/password_change.html', 
    'password_change_redirect': config.get_password_change_redirect(), 
    'password_change_form': config.get_password_change_form()}, name='baseacct-password-change'),
 url('^password_change/done/$', TemplateView.as_view(template_name='baseacct/password_change_done.html'), name='baseacct-password-change-done'),
 url('^reset/$', views.reset, {'template': 'baseacct/reset.html', 
    'reset_form': config.get_reset_form(), 
    'profile_model': config.get_profile_model()}, name='baseacct-reset'),
 url('^reset/(?P<key>\\w+)/$', views.reset, {'template': 'baseacct/reset_complete.html', 
    'reset_form': config.get_reset_form(), 
    'profile_model': config.get_profile_model()}, name='baseacct-reset-key')]