# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/stacktraces/platform.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import

def get_behavior_family_for_platform(platform):
    if platform in ('objc', 'cocoa', 'swift', 'native', 'c'):
        return 'native'
    if platform in ('javascript', 'node'):
        return 'javascript'
    return 'other'