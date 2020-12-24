# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/byte.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 225 bytes
from firestore.datatypes.base import Base

class Byte(Base):
    __doc__ = '\n    Firestore cloud db byte datatype. Up to 1,048,487 bytes (1 MiB - 89 bytes).\n    Only the first 1,500 bytes are considered by queries\n    '