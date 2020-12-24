# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/info/gianlucacosta/iris/vars.py
# Compiled at: 2017-10-18 20:54:09
# Size of source mod 2**32: 1758 bytes
"""
File-based management of variables.

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""
import os
from .io.utils import PathOperations

class VariablesService:
    __doc__ = '\n    Centralizes several file-based variables in one directory\n    '

    def __init__(self, variablesDirPath):
        """
        Instantiates the service, receiving the directory that
        will contain the variable-related files
        """
        self._variablesDirPath = variablesDirPath

    def getFlag(self, flagName):
        """
        Creates a flag having path <variables dir path><os.sep><flagName>
        """
        assert len(flagName) > 0
        return Flag(os.path.join(self._variablesDirPath, flagName))


class Flag:
    __doc__ = '\n    A Flag is a boolean variable whose value depends\n    on the existence of the underlying path: isActive()\n    returns true if and only if that path exists.\n\n    This concept can be very handy when using different\n    technologies, that use files as a simple communication\n    means.\n    '

    def __init__(self, path):
        self._path = path

    def getPath(self):
        return self._path

    def isActive(self):
        """
        Returns the value of the flag
        """
        return os.path.exists(self._path)

    def activate(self):
        """
        Sets the flag's value to true
        """
        PathOperations.touch(self._path)

    def deactivate(self):
        """
        Sets the flag's value to false
        """
        PathOperations.safeRemove(self._path)

    def flip(self):
        """
        Flips the state of the flag
        """
        if self.isActive():
            self.deactivate()
        else:
            self.activate()