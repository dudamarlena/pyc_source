# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/capabilities.py
# Compiled at: 2009-10-07 18:08:46
import sys

class Capabilities(object):
    __module__ = __name__

    def getframe(self):
        try:
            sys._getframe()
            return True
        except ValueError:
            return False

    getframe = property(getframe)

    def f_back(self):
        return self.getframe and hasattr(sys._getframe(), 'f_back')

    f_back = property(f_back)

    def settrace(self):
        try:
            sys.settrace(None)
            return True
        except NotImplementedError:
            return False

        return

    settrace = property(settrace)


c = Capabilities()