# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\util.py
# Compiled at: 2019-11-09 02:45:51
# Size of source mod 2**32: 547 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging
logger = logging.getLogger('enhterm')
from .lang import _

def needs_name(original_function):
    """Decorator that extracts the name argument."""

    def new_function(self, arg):
        name = arg['name'].strip()
        if len(name) == 0:
            self.error(_('A name needs to be provided'))
            return
        return original_function(self, arg, name)

    return new_function