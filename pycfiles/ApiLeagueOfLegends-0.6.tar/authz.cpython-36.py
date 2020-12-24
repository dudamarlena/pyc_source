# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jojo/.virtualenvs/apikit/lib/python3.6/site-packages/apikit/authz.py
# Compiled at: 2018-08-06 13:02:15
# Size of source mod 2**32: 667 bytes
from importlib import import_module
from werkzeug.exceptions import Forbidden

class Requirement(object):
    """Requirement"""

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, attr):
        real = getattr(self.wrapped, attr)
        return Requirement(real)

    def __call__(self, *args, **kwargs):
        fc = (self.wrapped)(*args, **kwargs)
        if fc is not True:
            raise Forbidden("Sorry, you're not permitted to do this.")
        return fc

    @classmethod
    def here(cls, t):
        return cls(import_module(t))