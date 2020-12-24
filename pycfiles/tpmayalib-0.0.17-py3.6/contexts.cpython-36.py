# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/contexts.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 505 bytes
"""
Module that contains functions and classes related with custom Maya Python contexts
"""
from __future__ import print_function, division, absolute_import
import contextlib, tpMayaLib as maya

@contextlib.contextmanager
def maya_no_undo():
    """
    Disable undo functionality during the context
    """
    try:
        maya.cmds.undoInfo(stateWithoutFlush=False)
        yield
    finally:
        maya.cmds.undoInfo(stateWithoutFlush=True)