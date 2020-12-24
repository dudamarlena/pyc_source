# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: rest_auth/tests/django_urls.py
# Compiled at: 2017-08-29 01:32:18
from django.conf.urls import url
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns
urlpatterns += [
 url('^logout/custom_query/$', views.logout, dict(redirect_field_name='follow')),
 url('^logout/next_page/$', views.logout, dict(next_page='/somewhere/')),
 url('^logout/next_page/named/$', views.logout, dict(next_page='password_reset')),
 url('^password_reset_from_email/$', views.password_reset, dict(from_email='staffmember@example.com')),
 url('^password_reset/custom_redirect/$', views.password_reset, dict(post_reset_redirect='/custom/')),
 url('^password_reset/custom_redirect/named/$', views.password_reset, dict(post_reset_redirect='password_reset')),
 url('^password_reset/html_email_template/$', views.password_reset, dict(html_email_template_name='registration/html_password_reset_email.html')),
 url('^reset/custom/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, dict(post_reset_redirect='/custom/')),
 url('^reset/custom/named/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, dict(post_reset_redirect='password_reset')),
 url('^password_change/custom/$', views.password_change, dict(post_change_redirect='/custom/')),
 url('^password_change/custom/named/$', views.password_change, dict(post_change_redirect='password_reset')),
 url('^admin_password_reset/$', views.password_reset, dict(is_admin_site=True)),
 url('^login_required/$', login_required(views.password_reset)),
 url('^login_required_login_url/$', login_required(views.password_reset, login_url='/somewhere/'))]