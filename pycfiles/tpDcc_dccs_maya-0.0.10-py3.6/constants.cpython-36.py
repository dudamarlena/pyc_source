# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/constants.py
# Compiled at: 2020-05-13 19:28:33
# Size of source mod 2**32: 498 bytes
"""
Module that contains constants definitions for tpDcc.dccs.maya
"""
from __future__ import print_function, division, absolute_import
from tpDcc.libs.python import python
if python.is_python2():
    from aenum import Enum
else:
    from enum import Enum

class DebugLevels(Enum):
    Disabled = 0
    Low = 1
    Mid = 2
    High = 3


class ScriptLanguages(Enum):
    Python = 0
    MEL = 1
    CSharp = 2
    CPlusPlus = 3
    Manifest = 4