# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/contexts.py
# Compiled at: 2020-05-02 23:38:23
# Size of source mod 2**32: 512 bytes
"""
Module that contains functions and classes related with custom Maya Python contexts
"""
from __future__ import print_function, division, absolute_import
import contextlib, tpDcc.dccs.maya as maya

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