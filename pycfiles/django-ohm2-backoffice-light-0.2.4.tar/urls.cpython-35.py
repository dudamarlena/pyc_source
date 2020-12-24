# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_backoffice_light/api/v1/urls.py
# Compiled at: 2017-12-28 20:46:57
# Size of source mod 2**32: 406 bytes
from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION >= (2, 0):
    from django.urls import include, re_path as url
else:
    from django.conf.urls import include, url
from . import views
app_name = 'ohm2_backoffice_light_api_v1'
urlpatterns = [
 url('^user-exist/$', views.user_exist, name='user_exist'),
 url('^is-password-secure/$', views.is_password_secure, name='is_password_secure')]