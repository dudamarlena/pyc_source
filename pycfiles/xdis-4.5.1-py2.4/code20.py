# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/codetype/code20.py
# Compiled at: 2020-04-26 21:30:06
from xdis.version_info import PYTHON_VERSION
from xdis.codetype.code15 import Code15, Code15FieldTypes
import types
from copy import deepcopy
Code2FieldTypes = deepcopy(Code15FieldTypes)
Code2FieldTypes.update({'co_freevars': (tuple, list), 'co_cellvars': (tuple, list)})

class Code2(Code15):
    """Class for a Python2 code object used when a Python 3 interpreter is
    working on Python2 bytecode. It also functions as an object that can be used
    to build or write a Python2 code object, since we allow mutable structures.
    When done mutating, call method freeze().

    For convenience in generating code objects, fields like
    `co_consts`, co_names which are (immutable) tuples in the end-result can be stored
    instead as (mutable) lists. Likewise the line number table `co_lnotab`
    can be stored as a simple list of offset, line_number tuples.
    """
    __module__ = __name__

    def __init__(self, co_argcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name, co_firstlineno, co_lnotab, co_freevars, co_cellvars):
        super(Code2, self).__init__(co_argcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name, co_firstlineno, co_lnotab)
        self.co_freevars = co_freevars
        self.co_cellvars = co_cellvars
        self.fieldtypes = Code2FieldTypes
        if type(self) == Code2:
            self.check()

    def to_native(self, opts={}):
        if not 2.0 <= PYTHON_VERSION <= 2.7:
            raise TypeError('Python Interpreter needs to be in range 2.0..2.7; is %s' % PYTHON_VERSION)
        code = deepcopy(self)
        code.freeze()
        try:
            code.check()
        except AssertionError(e):
            raise TypeError(e)

        return types.CodeType(code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags, code.co_code, code.co_consts, code.co_names, code.co_varnames, code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)


class Code2Compat(Code2):
    """A much more flexible version of Code. We don't require kwonlyargcount which
    doesn't exist. You can also fill in what you want and leave the rest blank.

    Call to_native() when done.
    """
    __module__ = __name__

    def __init__(self, co_argcount=0, co_nlocals=0, co_stacksize=0, co_flags=[], co_code=[], co_consts=[], co_names=[], co_varnames=[], co_filename='unknown', co_name='unknown', co_firstlineno=1, co_lnotab='', co_freevars=[], co_cellvars=[]):
        self.co_argcount = co_argcount
        self.co_nlocals = co_nlocals
        self.co_stacksize = co_stacksize
        self.co_flags = co_flags
        self.co_code = co_code
        self.co_consts = co_consts
        self.co_names = co_names
        self.co_varnames = co_varnames
        self.co_filename = co_filename
        self.co_name = co_name
        self.co_firstlineno = co_firstlineno
        self.co_lnotab = co_lnotab
        self.co_freevars = co_freevars
        self.co_cellvars = co_cellvars

    def __repr__(self):
        return '<code2 object %s at 0x%0x, file "%s", line %d>' % (self.co_name, id(self), self.co_filename, self.co_firstlineno)