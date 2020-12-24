# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/executable.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1072 bytes
from noval import _
from tkinter import messagebox
import noval.util.apputils as apputils, noval.util.strutils as strutils, os
UNKNOWN_VERSION_NAME = 'Unknown Version'

class Executable(object):

    def __init__(self, name, path):
        self._path = path
        self._install_path = os.path.dirname(self._path)
        self._name = name

    @property
    def Path(self):
        return self._path

    @property
    def InstallPath(self):
        return self._install_path

    @property
    def Version(self):
        return UNKNOWN_VERSION_NAME

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, name):
        self._name = name