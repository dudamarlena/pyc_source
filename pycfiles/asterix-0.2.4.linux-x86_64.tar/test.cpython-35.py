# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ingvij/Development/Personal/asterix/.venv/lib/python3.5/site-packages/asterix/test.py
# Compiled at: 2016-07-17 21:27:48
# Size of source mod 2**32: 524 bytes
""" Utility functions to help testing. """
from unittest.mock import Mock

class dummy(object):

    def __init__(self):
        self.components = {}

    def get(self, name, default=None):
        if name not in self.components:
            self.components[name] = Mock()
        return self.components[name]


class dummy_master(object):

    def __init__(self):
        setattr(self, '__components', dummy())

    def get(self, name):
        return getattr(self, '__components').components.get(name)