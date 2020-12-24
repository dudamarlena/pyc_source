# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Domlette.py
# Compiled at: 2006-08-22 11:28:10
"""
Abstraction module for Domlette usage.
Domlette is a DOM-like library tailored for use in XPath/XSLT.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
__all__ = [
 'implementation', 'NonvalParse', 'ValParse', 'Print', 'PrettyPrint', 'CanonicalPrint', 'GetAllNs', 'SeekNss', 'ConvertDocument', 'ValidatingReaderBase', 'NonvalidatingReaderBase', 'NoExtDtdReaderBase', 'EntityReaderBase', 'ValidatingReader', 'NonvalidatingReader', 'NoExtDtdReader', 'EntityReader']
import os, sys, cStringIO, warnings
from Ft.Xml import READ_EXTERNAL_DTD
from Ft.Xml import InputSource
from Lib.Print import Print, PrettyPrint, CanonicalPrint
from Lib.XmlString import XmlStrLStrip, XmlStrRStrip, XmlStrStrip, IsXmlSpace
from cDomlette import implementation, DOMImplementation, DocumentFragment, Document, Node, CharacterData, Attr, Element, Text, Comment, ProcessingInstruction, XPathNamespace
from cDomlette import NonvalParse, ValParse, ParseFragment
from cDomlette import GetAllNs, SeekNss

def parse(isrc, readExtDtd=READ_EXTERNAL_DTD):
    warnings.warn('parse() deprecated; use Parse()', DeprecationWarning, 2)
    return Parse(isrc, readExtDtd)


def nonvalParse(isrc, readExtDtd=READ_EXTERNAL_DTD):
    warnings.warn('nonvalParse() deprecated; use NonvalParse()', DeprecationWarning, 2)
    return NonvalParse(isrc, readExtDtd)


def valParse(isrc, readExtDtd=True):
    warnings.warn('valParse() deprecated; use ValParse()', DeprecationWarning, 2)
    return ValParse(isrc)


def ConvertDocument(oldDocument, documentURI=''):
    """
    Since foreign DOMs are not supported within 4Suite, this function
    lets users create a Domlette DOM from whatever DOM they are using.

    If the documentURI is not specified, it will try and get it from
    the document using DOM L3 attributes documentURI, then baseURI. If
    no URI is found, a warning is issued and a urn:uuid is generated
    for it.
    """
    if not documentURI:
        if hasattr(oldDocument, 'documentURI'):
            documentURI = oldDocument.documentURI
        elif hasattr(oldDocument, 'baseURI'):
            documentURI = oldDocument.baseURI
        else:
            from Ft.Lib import Uuid
            documentURI = 'urn:uuid:' + Uuid.UuidAsString(Uuid.GenerateUuid())
            warnings.warn('Document created without a URI', RuntimeWarning, 2)
    document = implementation.createRootNode(documentURI)
    for oldChild in oldDocument.childNodes:
        child = document.importNode(oldChild, 1)
        document.appendChild(child)

    return document


class SaxWalker:
    """
    Wrapper for a Saxlette parser that allows you to walk a Domlette
    tree and fire off SAX2 events as if parsing an XML source.
    """
    __module__ = __name__

    def __init__(self, node, baseUri=''):
        """
        node - the Domlette node to be walked
        baseUri - optional override for the baseUri to use in parsing
                  by default this is retrieved from the Domlette node
        """
        from xml.sax.handler import property_dom_node
        from Ft.Xml import Sax, InputSource
        if not baseUri:
            if hasattr(node, 'documentURI'):
                baseUri = node.documentURI
            elif hasattr(node, 'baseURI'):
                baseUri = node.baseURI
            else:
                raise TypeError('baseUri required')
        self.isrc = InputSource.DefaultFactory.fromStream(None, baseUri)
        self.parser = Sax.CreateParser()
        self.parser.setProperty(property_dom_node, node)
        return
        return

    def parse(self):
        """
        Execute the SAX2 parse phase (using Saxlette)
        """
        return self.parser.parse(self.isrc)

    def __getattr__(self, value):
        return getattr(self.parser, value)


class _Reader:
    """
    Base class for all XML readers.
    Subclassed by NonvalidatingReaderBase and ValidatingReaderBase.
    """
    __module__ = __name__

    def __init__(self, parseMethod, inputSourceFactory=None, args=(), kwargs=None):
        self.inputSourceFactory = inputSourceFactory or InputSource.DefaultFactory
        self.parseMethod = parseMethod
        self.kwargs = kwargs or {}
        self.args = args
        return

    def parse(self, inputSource):
        """
        Reads XML from an Ft.Xml.Inputsource.InputSource, and
        returns a Domlette document node.
        """
        if not isinstance(inputSource, InputSource.InputSource):
            raise TypeError('inputSource must be an instance of Ft.Xml.InputSource.InputSource')
        return self.parseMethod(inputSource, *self.args, **self.kwargs)

    def parseString(self, st, uri=None, *v_args, **kw_args):
        """
        Reads an XML document entity provided as an ordinary python
        byte string (the st argument), and returns a Domlette
        document node.  st cannot be a Unicode string.

        The document URI should be provided as the uri argument.
        This will be used in the resolution of system IDs in the DTD
        and document type declaration, and will be embedded in the
        Domlette nodes for use by the application, such as for
        resolution of relative URI references in XSLT's document(),
        xsl:import, and xsl:include, among others.
        """
        isrc = self.inputSourceFactory.fromString(st, uri, *v_args, **kw_args)
        return self.parse(isrc)

    def parseStream(self, stream, uri=None, *v_args, **kw_args):
        """
        Reads an XML document entity from a python file-like object
        (the stream argument), and returns a Domlette document node.

        The document URI should be provided as the uri argument.
        This will be used in the resolution of system IDs in the DTD
        and document type declaration, and will be embedded in the
        Domlette nodes for use by the application, such as for
        resolution of relative URI references in XSLT's document(),
        xsl:import, and xsl:include, among others.
        """
        isrc = self.inputSourceFactory.fromStream(stream, uri, *v_args, **kw_args)
        return self.parse(isrc)

    def parseUri(self, uri, *v_args, **kw_args):
        """
        Reads an XML document entity from a URI (the uri argument),
        and returns a Domlette document node.
        """
        isrc = self.inputSourceFactory.fromUri(uri, *v_args, **kw_args)
        return self.parse(isrc)


class ValidatingReaderBase(_Reader):
    """
    Base class to be used by all validating readers.
    Allows an InputSource factory to be specified.
    """
    __module__ = __name__

    def __init__(self, inputSourceFactory=None):
        _Reader.__init__(self, ValParse, inputSourceFactory)


class NonvalidatingReaderBase(_Reader):
    """
    Base class to be used by all non-validating readers.
    Allows an InputSource factory to be specified.
    Allows control over whether the external DTD subset is read.
    """
    __module__ = __name__

    def __init__(self, inputSourceFactory=None):
        _Reader.__init__(self, NonvalParse, inputSourceFactory, kwargs={'readExtDtd': READ_EXTERNAL_DTD})


class EntityReaderBase(_Reader):
    """
    Base class to be used by all readers which can accept well-formed EPEs.
    Non-validating only.
    Allows an InputSource factory to be specified.
    Allows control over whether the external DTD subset is read.
    """
    __module__ = __name__

    def __init__(self, inputSourceFactory=None):
        _Reader.__init__(self, ParseFragment, inputSourceFactory)


class NoExtDtdReaderBase(_Reader):
    """
    Base class to be used by all non-validating readers
    that do not need to read the external DTD subset.
    Allows an InputSource factory to be specified.
    """
    __module__ = __name__

    def __init__(self, inputSourceFactory=None):
        _Reader.__init__(self, NonvalParse, inputSourceFactory, kwargs={'readExtDtd': False})


ValidatingReader = ValidatingReaderBase()
ValidatingReader.__doc__ = '\nThe default validating reader instance, created from\nValidatingReaderBase() with no constructor arguments.\n\nUses the default InputSource factory. If you need to change it,\nreassign the inputSourceFactory attribute, or, preferably, just\ncreate a new ValidatingReaderBase instance.\n'
NonvalidatingReader = NonvalidatingReaderBase()
NonvalidatingReader.__doc__ = '\nThe default non-validating reader instance, created from\nNonvalidatingReaderBase() with no constructor arguments.\n\nUses the default InputSource factory. If you need to change it,\nreassign the inputSourceFactory attribute, or, preferably, just\ncreate a new NonvalidatingReaderBase instance.\n'
NoExtDtdReader = NoExtDtdReaderBase()
NoExtDtdReader.__doc__ = '\nThe default non-validating, external DTD subset-ignoring reader\ninstance, created from NoExtDtdReaderBase() with no constructor\narguments.\n\nUses the default InputSource factory. If you need to change it,\nreassign the inputSourceFactory attribute, or, preferably, just\ncreate a new NoExtDtdReaderBase instance.\n'
EntityReader = EntityReaderBase()
EntityReader.__doc__ = '\nNon-validating reader instance that accepts well-formed\nXML External Parsed Entities, created from\nEntityReader() with no constructor arguments.\n\nUses the default InputSource factory. If you need to change it,\nreassign the inputSourceFactory attribute, or, preferably, just\ncreate a new EntityReader instance.\n'

class DeprecatedReader:
    """
    Defined to support the old interfaces.
    If you're still using this, please upgrade to the newer API.
    """
    __module__ = __name__

    def __init__(self, resolveEntity=None, processIncludes=1):
        warnings.warn('You are using deprecated readers', DeprecationWarning, 2)
        self.resolveEntity = resolveEntity
        self.processIncludes = processIncludes
        self.inputSourceFactory = InputSource.DefaultFactory

    def fromUri(self, uri, baseUri='', ownerDoc=None, stripElements=None):
        """
        Creates a default InputSource from a URI (the uri argument).
        The baseUri and ownerDoc arguments are ignored.
        """
        src = InputSource.InputSource(None, uri, processIncludes=self.processIncludes, stripElements=stripElements)
        src = src.resolve(uri)
        return self._parseMethod[0](src)
        return

    def fromStream(self, stream, refUri='', ownerDoc=None, stripElements=None):
        """
        Creates a default InputSource from a python file-like object
        (the stream argument). The document URI should be provided as
        the refUri argument. This will be used in the resolution of
        system IDs in the DTD and document type declaration, and will
        be embedded in the Domlette nodes for use by the application,
        such as for resolution of relative URI references in XSLT's
        document(), xsl:import, and xsl:include, among others.
        """
        if not refUri:
            warnings.warn('InputSource created without a document URI', RuntimeWarning, 2)
        src = InputSource.InputSource(stream, refUri, processIncludes=self.processIncludes, stripElements=stripElements)
        return self._parseMethod[0](src)

    def fromString(self, st, refUri='', ownerDoc=None, stripElements=None):
        """
        Creates a default InputSource from an ordinary python byte
        string (the st argument). The document URI should be provided as
        the refUri argument. This will be used in the resolution of
        system IDs in the DTD and document type declaration, and will
        be embedded in the Domlette nodes for use by the application,
        such as for resolution of relative URI references in XSLT's
        document(), xsl:import, and xsl:include, among others.
        """
        if isinstance(st, unicode):
            st = st.encode('utf-8')
        stream = cStringIO.StringIO(st)
        if not refUri:
            warnings.warn('InputSource created without a document URI', RuntimeWarning, 2)
        rt = self.fromStream(stream, refUri, ownerDoc, stripElements)
        stream.close()
        return rt


class DEFAULT_NONVALIDATING_READER(DeprecatedReader):
    __module__ = __name__
    _parseMethod = (NonvalParse,)


class DEFAULT_VALIDATING_READER(DeprecatedReader):
    __module__ = __name__
    _parseMethod = (ValParse,)