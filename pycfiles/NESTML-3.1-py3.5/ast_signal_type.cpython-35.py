# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_signal_type.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 872 bytes
from enum import Enum

class ASTSignalType(Enum):
    __doc__ = '\n    This enum is used to describe the type of the emitted signal.\n    '
    SPIKE = 1
    CURRENT = 2