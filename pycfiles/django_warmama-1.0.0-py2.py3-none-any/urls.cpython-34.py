# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/urls.py
# Compiled at: 2015-05-08 19:56:04
# Size of source mod 2**32: 882 bytes
from django.conf.urls import url
from warmama import views
urlpatterns = [
 url('^slogin$', views.ServerLogin.as_view(), name='slogin'),
 url('^slogout$', views.ServerLogout.as_view(), name='slogout'),
 url('^scc$', views.ServerClientConnect.as_view(), name='scc'),
 url('^scd$', views.ServerClientDisconnect.as_view(), name='scd'),
 url('^smr$', views.ServerMatchReport.as_view(), name='smr'),
 url('^shb$', views.ServerHeartbeat.as_view(), name='shb'),
 url('^smuuid$', views.ServerMatchUUID.as_view(), name='smuuid'),
 url('^clogin$', views.ClientLogin.as_view(), name='clogin'),
 url('^clogout$', views.ClientLogout.as_view(), name='clogout'),
 url('^ccc$', views.ClientConnect.as_view(), name='ccc'),
 url('^chb$', views.ClientHeartbeat.as_view(), name='chb'),
 url('^auth$', views.ClientAuthenticate.as_view(), name='auth')]