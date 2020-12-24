# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/red5/protectedvod/interfaces.py
# Compiled at: 2009-08-19 12:31:49
from zope.interface import Interface

class IRed5ProtectedVodTool(Interface):
    """A view that implements a hmac algorithm for url signatures
    """
    __module__ = __name__

    def netConnectionUrl():
        """ returns the netConnectionUrl including path, signature and expire date"""
        pass

    def clip():
        """ returns url of video with hmac signature """
        pass