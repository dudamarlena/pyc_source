# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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