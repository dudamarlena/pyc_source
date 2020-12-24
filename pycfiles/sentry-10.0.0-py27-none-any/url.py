# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/validators/url.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.exceptions import PluginError
from sentry.http import is_valid_url

def URLValidator(value, **kwargs):
    if not value.startswith(('http://', 'https://')):
        raise PluginError('Not a valid URL.')
    if not is_valid_url(value):
        raise PluginError('Not a valid URL.')
    return value