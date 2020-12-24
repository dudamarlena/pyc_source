# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/integer.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 248 bytes
from firestore.datatypes.number import Number

class Integer(Number):
    __doc__ = '\n    64bit signed non decimal integer\n    '

    def __init__(self, *args, **kwargs):
        self.py_type = int
        (super(Integer, self).__init__)(*args, **kwargs)