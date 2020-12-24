# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcelor/Code/Work/djangoinfo/djangoinfo/apps/django_info/django_info/__init__.py
# Compiled at: 2012-12-11 14:53:55
VERSION = (0, 0, 3, 'alpha')
if len(VERSION) > 2 and VERSION[2] is not None:
    if isinstance(VERSION[2], int):
        str_version = '%s.%s.%s' % VERSION[:3]
    else:
        str_version = '%s.%s_%s' % VERSION[:3]
else:
    str_version = '%s.%s' % VERSION[:2]
__version__ = str_version