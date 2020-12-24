# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/replacement_method.py
# Compiled at: 2019-05-31 17:48:42
# Size of source mod 2**32: 406 bytes
from enum import Enum

class ReplacementMethod(Enum):
    generational_replacement = (0, )
    delete_last = 1