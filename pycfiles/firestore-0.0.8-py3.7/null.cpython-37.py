# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/null.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 253 bytes
from firestore.datatypes.base import Base

class Null(Base):
    __doc__ = '\n    Null mapping to python None globally unique object\n    '

    def __init__(self, *args, **kwargs):
        pass

    def __eq__(self, comparable):
        return NotImplemented