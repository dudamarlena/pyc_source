# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/image/interfaces.py
# Compiled at: 2009-09-04 10:39:07
from zope.interface import Interface

class IRichFileImageLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class IRichFileImageSite(Interface):
    """ Marker interface for sites with this product installed.
    """
    __module__ = __name__


class IImage(Interface):
    """
    """
    __module__ = __name__


class IImageable(Interface):
    """
    """
    __module__ = __name__