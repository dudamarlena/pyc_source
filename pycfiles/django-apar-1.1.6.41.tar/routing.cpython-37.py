# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/routing.py
# Compiled at: 2019-12-29 15:17:17
# Size of source mod 2**32: 195 bytes
from django.conf.urls import url
from aparnik.contrib.messaging.consumers import MessagingConsumer
app_name = 'aparnik'
websocket_urlpatterns = [
 url('^messaging/', MessagingConsumer)]