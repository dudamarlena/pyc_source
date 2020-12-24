# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/__init__.py
# Compiled at: 2020-04-17 19:39:02
# Size of source mod 2**32: 294 bytes
VERSION = (0, 3, 88, 'final')
if VERSION[(-1)] != 'final':
    __version__ = '.'.join(map(str, VERSION))
else:
    __version__ = '.'.join(map(str, VERSION[:-1]))
default_app_config = 'djconnectwise.apps.DjangoConnectwiseConfig'