# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/html.py
# Compiled at: 2019-08-16 12:27:43
from __future__ import absolute_import
try:
    from html import escape
except ImportError:
    from cgi import escape as _escape

    def escape(value):
        return _escape(value, True)