# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/django.py
# Compiled at: 2013-12-13 03:37:00
# Size of source mod 2**32: 308 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class Django(StackItem):
    __doc__ = '\n    Runs a django server.\n\n    Arguments:\n    * command str Command\n                  Default: python manage.py runserver\n    '
    ready_text = 'Starting development server'