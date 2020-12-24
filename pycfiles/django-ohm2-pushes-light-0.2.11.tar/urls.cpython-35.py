# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_pushes_light/api/v1/urls.py
# Compiled at: 2017-12-28 11:34:03
# Size of source mod 2**32: 504 bytes
from django.conf.urls import url, include
from . import settings
from . import views
app_name = 'ohm2_pushes_light_api_v1'
urlpatterns = []
if settings.ONESIGNAL_ENABLED:
    urlpatterns += [
     url('^gateways/onesignal/register-device/android/$', views.gateways_onesignal_register_device_android, name='gateways_onesignal_register_device_android'),
     url('^gateways/onesignal/register-device/ios/$', views.gateways_onesignal_register_device_ios, name='gateways_onesignal_register_device_ios')]