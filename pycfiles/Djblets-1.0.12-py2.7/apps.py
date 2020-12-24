# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/apps.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object

class WebAPIAppConfig(AppConfig):
    name = b'djblets.webapi'
    label = b'djblets_webapi'