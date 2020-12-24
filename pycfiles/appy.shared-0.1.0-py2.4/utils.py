# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/shared/utils.py
# Compiled at: 2008-02-21 11:38:58
import os, os.path, sys, traceback

class FolderDeleter:
    __module__ = __name__

    def delete(dirName):
        """Recursively deletes p_dirName."""
        dirName = os.path.abspath(dirName)
        for (root, dirs, files) in os.walk(dirName, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(dirName)

    delete = staticmethod(delete)


class Traceback:
    """Dumps the last traceback into a string."""
    __module__ = __name__

    def get():
        res = ''
        (excType, excValue, tb) = sys.exc_info()
        tbLines = traceback.format_tb(tb)
        for tbLine in tbLines:
            res += ' %s' % tbLine

        res += ' %s: %s' % (str(excType), str(excValue))
        return res

    get = staticmethod(get)