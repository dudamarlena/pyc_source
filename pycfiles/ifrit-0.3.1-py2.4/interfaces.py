# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ifrit/interfaces.py
# Compiled at: 2007-02-09 16:41:42
""" ifrit package interfaces

$Id: interfaces.py,v 1.2 2007/02/09 21:41:42 tseaver Exp $
"""
from zope.interface import Interface

class IStringParser(Interface):
    """ Utility interface for a parser which can be called passing a string.

    o Examples:  elementtree.ElementTree.XML
    """
    __module__ = __name__

    def __call__(xmlstring):
        """ Parse 'xmlstring', and return the root ElementTree node.
        """
        pass


class IStreamParser(Interface):
    """ Utility interface for a parser which can be called passing a stream.

    o Examples:  elementtree.ElementTree.parse
    """
    __module__ = __name__

    def __call__(xmlstream):
        """ Parse 'xmlstream', and return the root ElementTree node.
        """
        pass


class IElement(Interface):
    """ Adapter interface.
    """
    __module__ = __name__


class IElementFactory(Interface):
    """ Adapter factory interface.
    """
    __module__ = __name__

    def __call__(context):
        """ Adapt context to an element interface
        
        o Adapted object will provide an interface derived from IElement.
        """
        pass


class IXMLSerialization(Interface):
    """ Utility interface.
    """
    __module__ = __name__

    def serialize(buffer):
        """ Write an XML representation of 'context' into 'buffer'.
        """
        pass