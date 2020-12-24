# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/object/object_toolkit.py
# Compiled at: 2019-09-29 14:34:30
# Size of source mod 2**32: 140 bytes


class ObjectToolkit:

    @classmethod
    def funcs2applied(cls, obj, funcs):
        for f in funcs:
            f(obj)

        return obj