# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gcluster/clustering.py
# Compiled at: 2019-11-05 02:10:18
# Size of source mod 2**32: 217 bytes
from enum import Enum
from .graph import Graph

class Mode(Enum):
    STRONG = 1
    UNION = 2


def clustering(mode: Mode):
    if mode == Mode.STRONG:
        return 1
    if mode == Mode.UNION:
        return 2