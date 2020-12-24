# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/info/gianlucacosta/iris/io/utils.py
# Compiled at: 2017-10-18 20:54:09
# Size of source mod 2**32: 3079 bytes
"""
I/O utilities

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""
import os, shutil

class PathOperations:
    __doc__ = '\n    Encapsulates operations on paths\n    '

    @staticmethod
    def safeMakeDirs(path, mode=511):
        """
        Creates the given directory path, as well as intermediate directories.
        Catches any I/O exception, returning False in that case; otherwise,
        True is returned.
        """
        try:
            os.makedirs(path, mode)
            return True
        except OSError:
            return False

    @staticmethod
    def safeRemove(path):
        """
        Removes the given file, returning true if the
        operation was successful.

        Any I/O exception is caught.
        """
        try:
            os.remove(path)
            return True
        except OSError:
            return False

    @staticmethod
    def touch(path):
        """
        Creates the given path as a file, also creating
        intermediate directories if required.
        """
        parentDirPath = os.path.dirname(path)
        PathOperations.safeMakeDirs(parentDirPath)
        with open(path, 'wb'):
            pass

    @staticmethod
    def safeRmTree(rootPath):
        """
        Deletes a tree and returns true if it was correctly deleted
        """
        shutil.rmtree(rootPath, True)
        return not os.path.exists(rootPath)

    @staticmethod
    def linearWalk(rootPath, currentDirFilter=None):
        """
        Returns a list of LinearWalkItem's, one for each file in the tree whose root is "rootPath".

        The parameter "currentDirFilter" is a method applied
        to every tuple (dirPath, dirNames, fileNames) automatically processed by os.walk():

        --it can modify its "dirNames" parameter, so as to prevent
          them to be processed later (just as in os.walk())

        --it can modify its "fileNames" parameter, so as to alter the
          global result linearWalk() (because it only returns files)

        --if it returns True, the files in "fileNames" will be added to the global result
          of linearWalk(); otherwise, they won't be added

        If no filter is passed, all the files are automatically added to the result.
        """
        for dirTuple in os.walk(rootPath):
            dirPath, dirNames, fileNames = dirTuple
            if currentDirFilter is not None and not currentDirFilter(dirPath, dirNames, fileNames):
                pass
            else:
                for fileName in fileNames:
                    yield LinearWalkItem(dirPath, fileName)


class LinearWalkItem:
    __doc__ = '\n    An item created by PathOperations.linearWalk()\n    '

    def __init__(self, dirPath, baseName):
        self.dirPath = dirPath
        self.baseName = baseName

    def getPath(self):
        """
        Returns the path of the item, obtained by joining its dir path and its basename
        """
        return os.path.join(self.dirPath, self.baseName)