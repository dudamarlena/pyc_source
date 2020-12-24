# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/codetype/code13.py
# Compiled at: 2020-04-24 01:34:34
from xdis.version_info import PYTHON3, PYTHON_VERSION
from xdis.codetype.base import CodeBase
import inspect, types
from copy import deepcopy
Code13FieldTypes = {'co_argcount': int, 'co_nlocals': int, 'co_flags': int, 'co_code': (str, list, tuple), 'co_consts': (tuple, list), 'co_names': (tuple, list), 'co_varnames': (tuple, list), 'co_filename': (str, unicode), 'co_name': (str, unicode)}

class Code13(CodeBase):
    """Class for a Python 1.0 .. 1.4 code object used for Python interpreters other than 1.0 .. 1.4

    For convenience in generating code objects, fields like
    `co_consts`, co_names which are (immutable) tuples in the end-result can be stored
    instead as (mutable) lists. Likewise the line number table `co_lnotab`
    can be stored as a simple list of offset, line_number tuples.
    """
    __module__ = __name__

    def __init__(self, co_argcount, co_nlocals, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name):
        self.co_argcount = co_argcount
        self.co_nlocals = co_nlocals
        self.co_flags = co_flags
        self.co_code = co_code
        self.co_consts = co_consts
        self.co_names = co_names
        self.co_varnames = co_varnames
        self.co_filename = co_filename
        self.co_name = co_name
        self.fieldtypes = Code13FieldTypes
        if type(self) == Code13:
            self.check()

    def check(self):
        for (field, fieldtype) in self.fieldtypes.items():
            val = getattr(self, field)
            if isinstance(fieldtype, tuple):
                assert type(val) in fieldtype, '%s should be one of the types %s; is type %s' % (field, fieldtype, type(val))
            else:
                assert isinstance(val, fieldtype), '%s should have type %s; is type %s' % (field, fieldtype, type(val))

    def freeze(self):
        for field in ('co_consts co_names co_varnames').split():
            val = getattr(self, field)
            if isinstance(val, list):
                setattr(self, field, tuple(val))

        return self

    def replace(self, **kwargs):
        """
        Return a copy of the code object with new values for the specified fields.

        This is analoguous to the method added to types.CodeType in Python 3.8.
        """
        code = deepcopy(self)
        for (field, value) in kwargs.items():
            if not hasattr(self, field):
                raise TypeError("Code object %s doesn't have field %s" % (type(self), self))
            setattr(code, field, value)

        return code