# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/SafeWriteFile.py
# Compiled at: 2007-11-06 15:08:00
from types import StringType
from shutil import copy2
from string import find
from os import rename

class ObjectNotAllowed(Exception):
    pass


class InvalidMode(Exception):
    pass


class SafeWriteFile:

    def __init__(self, newname, realname, mode='w', bufsize=-1):
        if type(newname) != StringType:
            raise ObjectNotAllowed(newname)
        if type(realname) != StringType:
            raise ObjectNotAllowed(realname)
        if find(mode, 'r') >= 0:
            raise InvalidMode(mode)
        if find(mode, 'a') >= 0 or find(mode, '+') >= 0:
            copy2(realname, newname)
        self.fobj = open(newname, mode, bufsize)
        self.newname = newname
        self.realname = realname
        self.__abort = 0

    def close(self):
        self.fobj.close()
        if not (self.closed and self.__abort):
            rename(self.newname, self.realname)

    def abort(self):
        self.__abort = 1

    def __del__(self):
        self.abort()
        del self.fobj

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except:
            return eval('self.fobj.' + attr)


if __name__ == '__main__':
    import time
    f = SafeWriteFile('sf.new', 'sf.data')
    f.write('test\n')
    f.flush()
    time.sleep(1)
    f.close()