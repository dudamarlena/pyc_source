# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/tickets/api/urls-conversations.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 317 bytes
from django.conf.urls import url, include
from .views import TicketConversationListAPIView, TicketConversationCreateAPIView
app_name = 'tickets'
urlpatterns = [
 url('^$', (TicketConversationListAPIView.as_view()), name='list'),
 url('^create/$', (TicketConversationCreateAPIView.as_view()), name='create')]