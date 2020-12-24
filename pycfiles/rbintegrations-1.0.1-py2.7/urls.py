# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/trello/urls.py
# Compiled at: 2020-01-07 04:31:42
"""URL definitions for the Trello integration."""
from __future__ import unicode_literals
from django.conf.urls import include, url
from rbintegrations.trello.views import TrelloCardSearchView
localsite_urlpatterns = [
 url(b'^card-search/(?P<review_request_id>\\d+)/$', TrelloCardSearchView.as_view(), name=b'trello-card-search')]
urlpatterns = [
 url(b'^s/(?P<local_site_name>[\\w\\.-]+)/', include(localsite_urlpatterns))]
urlpatterns += localsite_urlpatterns