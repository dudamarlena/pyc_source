# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/native/object_tools.py
# Compiled at: 2019-04-03 10:23:12
# Size of source mod 2**32: 118 bytes


class ObjectToolkit:

    @classmethod
    def obj2cls(cls, obj):
        return obj.__class__


obj2cls = ObjectToolkit.obj2cls