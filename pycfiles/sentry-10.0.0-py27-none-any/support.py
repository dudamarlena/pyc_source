# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/support.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import

def get_support_mail():
    """Returns the most appropriate support email address"""
    from sentry.options import get
    return get('system.support-email') or get('system.admin-email') or None