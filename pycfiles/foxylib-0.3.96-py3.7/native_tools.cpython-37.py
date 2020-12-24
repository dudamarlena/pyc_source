# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/native/native_tools.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 1289 bytes
from functools import reduce
from future.utils import lmap
from foxylib.tools.function.function_tool import funcs2piped

class NoneToolkit:

    @classmethod
    def is_none(cls, x):
        return x is None

    @classmethod
    def is_not_none(cls, x):
        return x is not None

    @classmethod
    def is_all_none(cls, l):
        return all(map(cls.is_none, l))


class BooleanToolkit:

    @classmethod
    def parse_sign2bool(cls, s):
        if s == '+':
            return True
        if s == '-':
            return False
        raise Exception('Invalid sign: {0}'.format(s))

    @classmethod
    def parse2nullboolean(cls, s):
        if any(filter(lambda x: s is x, {None, True, False})):
            return s
        else:
            return s or None
        s_lower = s.lower()
        if s_lower.isdecimal():
            v = int(s_lower)
            return bool(v)
        if s_lower in {'y', 't', 'true', 'yes'}:
            return True
        if s_lower in {'n', 'no', 'false', 'f'}:
            return False


class IntToolkit:

    @classmethod
    def parse_sign2int(cls, s):
        if not s:
            return 1
        if s == '+':
            return 1
        if s == '-':
            return -1
        raise Exception('Invalid sign: {0}'.format(s))


is_none = NoneToolkit.is_none
is_not_none = NoneToolkit.is_not_none
is_all_none = NoneToolkit.is_all_none