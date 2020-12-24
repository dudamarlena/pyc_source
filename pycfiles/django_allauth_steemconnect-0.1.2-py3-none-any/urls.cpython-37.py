# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ohing/workspace/steempumpkin/api/steemconnect_provider/providers/steemconnect/urls.py
# Compiled at: 2018-12-25 00:10:24
# Size of source mod 2**32: 177 bytes
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import SteemConnectProvider
urlpatterns = default_urlpatterns(SteemConnectProvider)