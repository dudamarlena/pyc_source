# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/codetype/code38.py
# Compiled at: 2020-04-20 10:24:57
from xdis.version_info import PYTHON_VERSION
from xdis.codetype.code30 import Code3, Code3FieldTypes
import types
from copy import deepcopy
Code38FieldNames = '\n        co_argcount\n        co_posonlyargcount\n        co_kwonlyargcount\n        co_nlocals\n        co_stacksize\n        co_flags\n        co_code\n        co_consts\n        co_names\n        co_varnames\n        co_filename\n        co_name\n        co_firstlineno\n        co_lnotab\n        co_freevars\n        co_cellvars\n'
Code38FieldTypes = deepcopy(Code3FieldTypes)
Code38FieldTypes.update({'co_posonlyargcount': int})

class Code38(Code3):
    """Class for a Python 3.8+ code object used when a Python interpreter less than 3.8 is
    working on Python3 bytecode. It also functions as an object that can be used
    to build or write a Python3 code object, since we allow mutable structures.

    When done mutating, call method to_native().

    For convenience in generating code objects, fields like
    `co_consts`, co_names which are (immutable) tuples in the end-result can be stored
    instead as (mutable) lists. Likewise the line number table `co_lnotab`
    can be stored as a simple list of offset, line_number tuples.
    """
    __module__ = __name__

    def __init__(self, co_argcount, co_posonlyargcount, co_kwonlyargcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name, co_firstlineno, co_lnotab, co_freevars, co_cellvars):
        super(Code38, self).__init__(co_argcount, co_kwonlyargcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name, co_firstlineno, co_lnotab, co_freevars, co_cellvars)
        self.co_posonlyargcount = co_posonlyargcount
        self.fieldtypes = Code38FieldTypes
        if type(self) == Code38:
            self.check()

    def to_native(self):
        if not PYTHON_VERSION >= 3.8:
            raise TypeError('Python Interpreter needs to be in 3.8 or greater; is %s' % PYTHON_VERSION)
        code = deepcopy(self)
        code.freeze()
        try:
            code.check()
        except AssertionError(e):
            raise TypeError(e)

        return types.CodeType(code.co_argcount, code.co_posonlyargcount, code.co_kwonlyargcount, code.co_nlocals, code.co_stacksize, code.co_flags, code.co_code, code.co_consts, code.co_names, code.co_varnames, code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)