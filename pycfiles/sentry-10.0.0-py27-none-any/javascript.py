# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/javascript.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from sentry.utils.safe import get_path

def has_sourcemap(event):
    if event.platform not in ('javascript', 'node'):
        return False
    for exception in get_path(event.data, 'exception', 'values', filter=True, default=()):
        for frame in get_path(exception, 'stacktrace', 'frames', filter=True, default=()):
            if 'sourcemap' in (frame.get('data') or ()):
                return True

    return False