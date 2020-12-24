# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/streaming/interfaces.py
# Compiled at: 2009-09-14 10:15:09
from zope.interface import Interface

class IRichFileStreamingLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class IRichFileStreamingSite(Interface):
    """ Marker interface for sites with this product installed.
    """
    __module__ = __name__


class IStreaming(Interface):
    """
    """
    __module__ = __name__


class IStreamingAudio(IStreaming):
    """
    """
    __module__ = __name__


class IStreamingVideo(IStreaming):
    """
    """
    __module__ = __name__


class IStreamable(Interface):
    """
    """
    __module__ = __name__


class ICallBackView(Interface):
    """
    """
    __module__ = __name__

    def conv_done_xmlrpc(status):
        """
        """
        pass