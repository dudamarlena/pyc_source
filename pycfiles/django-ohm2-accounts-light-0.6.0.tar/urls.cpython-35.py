# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_accounts_light/api/v1/urls.py
# Compiled at: 2017-12-28 11:31:00
# Size of source mod 2**32: 2232 bytes
from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION >= (2, 0):
    from django.urls import include, re_path as url
else:
    from django.conf.urls import include, url
from . import settings
from . import views
app_name = 'ohm2_accounts_light_api_v1'
urlpatterns = [
 url('^signup/$', views.signup, name='signup'),
 url('^login/$', views.login, name='login'),
 url('^logout/$', views.logout, name='logout'),
 url('^signup-and-get-token/$', views.signup_and_get_token, name='signup_and_get_token'),
 url('^login-and-get-token/$', views.login_and_get_token, name='login_and_get_token')]
if settings.INCLUDE_PATCHED_URLS:
    urlpatterns += [
     url('^signup-and-get-token/patched/$', views.signup_and_get_token_patched, name='signup_and_get_token_patched'),
     url('^login-and-get-token/patched/$', views.login_and_get_token_patched, name='login_and_get_token_patched')]
urlpatterns += [
 url('^send-password-reset-link/$', views.send_password_reset_link, name='send_password_reset_link'),
 url('^set-password-reset/$', views.set_password_reset, name='set_password_reset'),
 url('^set-password-reset-and-get-token/$', views.set_password_reset_and_get_token, name='set_password_reset_and_get_token'),
 url('^update-user-information/$', views.update_user_information, name='update_user_information')]
if settings.ENABLE_SOCIAL_LOGIN:
    urlpatterns += [
     url('^', include('social.apps.django_app.urls', namespace='social'))]
if settings.FACEBOOK_LOGIN:
    urlpatterns += [
     url('^facebook/login-and-get-token/$', views.facebook_login_and_get_token, name='facebook_login_and_get_token')]
    if settings.INCLUDE_PATCHED_URLS:
        urlpatterns += [
         url('^facebook/login-and-get-token/patched/$', views.facebook_login_and_get_token_patched, name='facebook_login_and_get_token_patched')]
if settings.GOOGLE_PLUS_LOGIN:
    urlpatterns += [
     url('^google-plus/login-and-get-token/$', views.google_plus_login_and_get_token, name='google_plus_login_and_get_token')]
    if settings.INCLUDE_PATCHED_URLS:
        urlpatterns += [
         url('^google-plus/login-and-get-token/patched/$', views.google_plus_login_and_get_token_patched, name='google_plus_login_and_get_token_patched')]