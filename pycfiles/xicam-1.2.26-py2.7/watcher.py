# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\watcher.py
# Compiled at: 2018-08-27 17:21:07
from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import Qt
import os

class newfilewatcher(QtCore.QFileSystemWatcher):
    newFilesDetected = QtCore.Signal(str, list)

    def __init__(self):
        super(newfilewatcher, self).__init__()
        self.childrendict = dict()
        self.directoryChanged.connect(self.checkdirectory)

    def addPath(self, path):
        super(newfilewatcher, self).addPath(path)
        self.childrendict[path] = set(os.listdir(path))

    def checkdirectory(self, path):
        updatedchildren = set(os.listdir(path))
        newchildren = updatedchildren - self.childrendict[path]
        self.childrendict[path] = updatedchildren
        self.newFilesDetected.emit(path, list(newchildren))