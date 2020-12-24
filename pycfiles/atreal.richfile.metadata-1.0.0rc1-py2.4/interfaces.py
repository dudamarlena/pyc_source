# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/interfaces.py
# Compiled at: 2009-09-04 10:38:20
from zope.interface import Interface

class IRichFileMetadataLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class IRichFileMetadataSite(Interface):
    """ Marker interface for sites with this product installed.
    """
    __module__ = __name__


class IMetadata(Interface):
    """
    """
    __module__ = __name__


class IMetadataExtractor(Interface):
    """
    """
    __module__ = __name__


class IExtractorWrapper(Interface):
    """ Interface for an extractor's wrapper """
    __module__ = __name__

    def available(self):
        """ True if the matching lib/binary is available"""
        pass

    def bestMimetypes(self):
        """ Return the more effective mimetypes list supported by the extractor """
        pass

    def supportedMimetypes(self):
        """ Return the mimetypes list supported by the extractor """
        pass

    def extract(self, myfile):
        """ Return a mapping filled with the file metadatas """
        pass