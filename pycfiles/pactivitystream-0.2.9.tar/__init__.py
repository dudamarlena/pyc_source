# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jason/django-activity-stream/activity_stream/__init__.py
# Compiled at: 2011-12-31 17:04:52
VERSION = (0, 2, 9)

def get_version():
    return '%s.%s.%s' % (VERSION[0], VERSION[1], VERSION[2])


__version__ = get_version()