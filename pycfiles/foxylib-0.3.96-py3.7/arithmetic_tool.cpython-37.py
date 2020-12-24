# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/arithmetic/arithmetic_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 256 bytes


class ArithmeticTool:

    @classmethod
    def divide_and_ceil(cls, v, d):
        q = v // d
        r = v % d
        return q + (1 if r else 0)

    @classmethod
    def modulo_d(cls, v, d):
        r = v % d
        if r == 0:
            return d
        return r