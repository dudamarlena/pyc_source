# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/oauth/apps.py
# Compiled at: 2020-02-11 04:03:56
"""The app definition for reviewboard.oauth."""
from __future__ import unicode_literals
try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object

class OAuthAppConfig(AppConfig):
    name = b'reviewboard.oauth'
    label = b'reviewboard_oauth'