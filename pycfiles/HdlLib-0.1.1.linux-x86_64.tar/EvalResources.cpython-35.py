# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/EvalResources.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 707 bytes
import sys, os, logging, re, math
from HdlLib.Utilities.ErrorHandlers import ToolError, ExecError
from HdlLib.SysGen.Module import Module
from HdlLib.SysGen.Signal import Signal

class ResourceUsage:

    def __init__(self):
        """
                Initialize resource dictionary
                """
        self.ResourceDict = {}

    def Eval(self, Mod):
        """
                Execute logic synthesis of a given module and return resource usage object.
                """
        return self.ResourceDict