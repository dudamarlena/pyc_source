# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haoda/backend/common.py
# Compiled at: 2020-04-26 02:44:08
# Size of source mod 2**32: 323 bytes
from typing import NamedTuple
import enum
__all__ = ('Cat', 'Arg')

class Cat(enum.Enum):
    SCALAR = 0
    MMAP = 1
    ISTREAM = 2
    OSTREAM = 3


class Arg(NamedTuple):
    cat: Cat
    name: str
    port: str
    ctype: str
    width: int