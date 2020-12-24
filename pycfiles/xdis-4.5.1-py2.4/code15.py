# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/codetype/code15.py
# Compiled at: 2020-04-26 21:30:06
from xdis.version_info import PYTHON3, PYTHON_VERSION
from xdis.codetype.code13 import Code13, Code13FieldTypes
import inspect, types
from copy import deepcopy
Code15FieldTypes = deepcopy(Code13FieldTypes)
Code15FieldTypes.update({'co_stacksize': int, 'co_firstlineno': int, 'co_lnotab': (str, dict)})

class Code15(Code13):
    """Class for a Python 1.5 code object used for Python interpreters other than 1.5.

    For convenience in generating code objects, fields like
    `co_consts`, co_names which are (immutable) tuples in the end-result can be stored
    instead as (mutable) lists. Likewise the line number table `co_lnotab`
    can be stored as a simple list of offset, line_number tuples.
    """
    __module__ = __name__

    def __init__(self, co_argcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name, co_firstlineno, co_lnotab):
        super(Code15, self).__init__(co_argcount, co_nlocals, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name)
        self.co_stacksize = co_stacksize
        self.co_firstlineno = co_firstlineno
        self.co_lnotab = co_lnotab
        self.fieldtypes = Code15FieldTypes
        if type(self) == Code15:
            self.check()

    def decode_lineno_tab(self):
        line_number, line_number_diff = self.co_firstlineno, 0
        (offset, offset_diff) = (0, 0)
        uncompressed_lnotab = {offset: line_number}
        if not hasattr(self.co_lnotab, '__len__'):
            raise TypeError('line number table should have a type with a length; is %s' % type(self.co_lnotab))
        for i in range(0, len(self.co_lnotab), 2):
            offset_diff = self.co_lnotab[i]
            line_number_diff = self.co_lnotab[(i + 1)]
            if not isinstance(offset_diff, int):
                offset_diff = ord(offset_diff)
                line_number_diff = ord(line_number_diff)
            assert offset_diff < 256
            if offset_diff == 255:
                continue
            assert line_number_diff < 256
            if line_number_diff == 255:
                continue
            line_number += line_number_diff
            offset += offset_diff
            (line_number_diff, offset_diff) = (0, 0)
            uncompressed_lnotab[offset] = line_number

        self.co_lnotab = uncompressed_lnotab

    def encode_lineno_tab(self):
        co_lnotab = ''
        prev_line_number = self.co_firstlineno
        prev_offset = 0
        for (offset, line_number) in self.co_lnotab:
            offset_diff = offset - prev_offset
            line_diff = line_number - prev_line_number
            prev_offset = offset
            prev_line_number = line_number
            while offset_diff >= 256:
                co_lnotab.append(chr(255))
                co_lnotab.append(chr(0))
                offset_diff -= 255

            while line_diff >= 256:
                co_lnotab.append(chr(0))
                co_lnotab.append(chr(255))
                line_diff -= 255

            co_lnotab += chr(offset_diff)
            co_lnotab += chr(line_diff)

        self.co_lnotab = co_lnotab

    def freeze(self):
        for field in ('co_consts co_names co_varnames co_freevars co_cellvars').split():
            val = getattr(self, field)
            if isinstance(val, list):
                setattr(self, field, tuple(val))

        if isinstance(self.co_lnotab, dict):
            d = self.co_lnotab
            self.co_lnotab = sorted(zip(d.keys(), d.values()), key=lambda tup: tup[0])
        if isinstance(self.co_lnotab, list):
            self.encode_lineno_tab()
        self.frozen = True
        return self