# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/systemd_dbus/__init__.py
# Compiled at: 2016-06-24 02:07:59
VERSION = (0, 0, 3)

def get_version():
    version = '%s.%s.%s' % (VERSION[0], VERSION[1], VERSION[2])
    return version