# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tidal_dl\check.py
# Compiled at: 2019-08-18 23:21:57
# Size of source mod 2**32: 698 bytes
import os
from aigpy import fileHelper

class CheckTool(object):

    def __init__(self):
        self.paths = []

    def isInErr(self, index, errIndex):
        for i in errIndex:
            if i == index:
                return True

        return False

    def clear(self):
        self.paths = []

    def addPath(self, path):
        self.paths.append(path)

    def checkPaths(self):
        index = 0
        flag = False
        errIndex = []
        for path in self.paths:
            if fileHelper.getFileSize(path) <= 0:
                errIndex.append(index)
                flag = True
            index = index + 1

        return (
         flag, errIndex)