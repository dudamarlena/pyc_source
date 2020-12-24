# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/autodestroy.py
# Compiled at: 2014-09-11 03:18:50
from twisted.web.static import File
import os

class FileAutoDestroy(File):
    """special twisted.web.static.File resource subclass
    to make it auto destroy the file once served
    """

    def open(self):
        return AutodestroyFile(self.path, 'r')


class AutodestroyFile(file):
    """a simple file like object that will autodestroy when you close() it...
    """

    def close(self):
        """we just make sure that the file will be destroyed when closed...
        """
        super(AutodestroyFile, self).close()
        os.unlink(self.name)