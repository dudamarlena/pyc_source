# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/constants.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 622 bytes
"""
Module that contains constants definitions for tpMayaLib
"""
from __future__ import print_function, division, absolute_import
from tpPyUtils import enum

class DebugLevel(enum.Enum):
    pass


class ScriptLanguage(enum.Enum):
    pass


class DebugLevels(enum.EnumGroup):
    Disabled = DebugLevel(0)
    Low = DebugLevel()
    Mid = DebugLevel()
    High = DebugLevel()


class ScriptLanguages(enum.EnumGroup):
    Python = ScriptLanguage()
    MEL = ScriptLanguage()
    CSharp = ScriptLanguage()
    CPlusPlus = ScriptLanguage()
    Manifest = ScriptLanguage()