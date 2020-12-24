# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./common/FileUtil.py
# Compiled at: 2013-10-19 00:37:17
import os

def getParent(path):
    return os.path.normpath(path)[:path.rfind(os.path.sep)]


def mkdirs(path):
    tmpPath = path
    pathStack = []
    while not os.path.lexists(tmpPath):
        pathStack.insert(0, tmpPath)
        tmpPath = os.path.normpath(tmpPath)[:tmpPath.rfind(os.path.sep)]

    for tmpPath in pathStack:
        try:
            os.mkdir(tmpPath)
        except OSError:
            if os.path.lexists(tmpPath):
                continue
            else:
                raise