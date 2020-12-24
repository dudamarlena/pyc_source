# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/streaming/convert.py
# Compiled at: 2009-09-14 10:15:09
from zope.interface import implements
from Products.Five import BrowserView
from atreal.richfile.streaming.interfaces import ICallBackView, IStreamable

class CallBackView(BrowserView):
    """
    """
    __module__ = __name__
    implements(ICallBackView)

    def conv_done_xmlrpc(self, status):
        """
        """
        IStreamable(self.context)._storeStreaming(status)