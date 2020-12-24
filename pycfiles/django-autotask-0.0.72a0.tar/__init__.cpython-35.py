# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/__init__.py
# Compiled at: 2020-05-12 17:39:24
# Size of source mod 2**32: 227 bytes
VERSION = (0, 0, 72, 'alpha')
if VERSION[(-1)] != 'final':
    __version__ = '.'.join(map(str, VERSION))
else:
    __version__ = '.'.join(map(str, VERSION[:-1]))