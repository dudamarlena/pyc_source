# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/django_oopviews/__init__.py
# Compiled at: 2008-10-01 14:10:06
VERSION = (0, 2, 0, 'final', 0)

def get_version():
    v = '%d.%d.%d' % VERSION[:3]
    if VERSION[3] != 'final':
        v = '%s%s%d' % (v, VERSION[3], VERSION[4])
    return v