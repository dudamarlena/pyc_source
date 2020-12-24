# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/das-g/hsr/dev/osmaxx/drf-utm-zone-info/utm_zone_info/urls.py
# Compiled at: 2017-01-12 05:31:18
# Size of source mod 2**32: 158 bytes
from django.conf.urls import url
from utm_zone_info import views
urlpatterns = [
 url('^utm-zone-info/$', views.utm_zone_info, name='utm-zone-info')]