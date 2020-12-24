# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/.virtualenvs/apikit/lib/python3.6/site-packages/apikit/authz.py
# Compiled at: 2018-08-06 13:02:15
# Size of source mod 2**32: 667 bytes
from importlib import import_module
from werkzeug.exceptions import Forbidden

class Requirement(object):
    __doc__ = ' Checks a function call and raises an exception if the\n    function returns a non-True value. '

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