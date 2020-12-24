# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Lib\XmlPrinter.py
# Compiled at: 2006-04-12 16:06:10
__doc__ = '\nThis module supports document serialization in XML syntax.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import cStreamWriter

class XmlPrinter:
    """
    An XmlPrinter instance provides functions for serializing an XML or
    XML-like document to a stream, based on SAX-like event calls
    initiated by an Ft.Xml.Lib.Print.PrintVisitor instance.

    The methods in this base class attempt to emit a well-formed parsed
    general entity conformant to XML 1.0 syntax, with no extra
    whitespace added for visual formatting. Subclasses may emit
    documents conformant to other syntax specifications or with
    additional whitespace for indenting.

    The degree of well-formedness of the output depends on the data
    supplied in the event calls; no checks are done for conditions that
    would result in syntax errors, such as two attributes with the same
    name, "--" in a comment, etc. However, attribute() will do nothing
    if the previous event was not startElement(), thus preventing
    spurious attribute serializations.
    """
    __module__ = __name__

    def __init__(self, stream, encoding):
        """
        stream must be a file-like object open for writing binary
        data. encoding specifies the encoding which is to be used for
        writing to the stream.
        """
        self.stream = sw = cStreamWriter.StreamWriter(stream, encoding)
        self.encoding = encoding
        self.writeAscii = sw.writeAscii
        self.writeEncode = sw.writeEncode
        self.writeEscape = sw.writeEscape
        self.reset()
        return

    def reset(self):
        """Sets the writer state as if it were a brand new instance"""
        self._inElement = False
        return

    def startDocument(self, version='1.0', standalone=None):
        """
        Handles a startDocument event.

        Writes XML declaration or text declaration to the stream.
        """
        self.writeAscii('<?xml version="%s" encoding="%s"' % (version, self.encoding))
        if standalone is not None:
            self.writeAscii(' standalone="%s"' % standalone)
        self.writeAscii('?>\n')
        return
        return

    def endDocument(self):
        """
        Handles an endDocument event.

        Writes any necessary final output to the stream.
        """
        if self._inElement:
            self.writeAscii('/>')
        return

    def doctype(self, name, publicId, systemId):
        """
        Handles a doctype event.

        Writes a document type declaration to the stream.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        if publicId and systemId:
            self.writeAscii('<!DOCTYPE ')
            self.writeEncode(name, 'document type name')
            self.writeAscii(' PUBLIC "')
            self.writeEncode(publicId, 'document type public-id')
            self.writeAscii('" "')
            self.writeEncode(systemId, 'document type system-id')
            self.writeAscii('">\n')
        elif systemId:
            self.writeAscii('<!DOCTYPE ')
            self.writeEncode(name, 'document type name')
            self.writeAscii(' SYSTEM "')
            self.writeEncode(systemId, 'document type system-id')
            self.writeAscii('">\n')
        return

    def startElement(self, namespaceUri, tagName, namespaces, attributes):
        """
        Handles a startElement event.

        Writes part of an element's start-tag or empty-element tag to
        the stream, and closes the start tag of the previous element,
        if one remained open. Writes the xmlns attributes for the given
        dictionary of namespaces, and invokes attribute() as neeeded to
        write the given dictionary of attributes.

        The namespaceUri argument is ignored in this class.
        """
        if self._inElement:
            self.writeAscii('>')
        else:
            self._inElement = True
        self.writeAscii('<')
        self.writeEncode(tagName, 'start-tag name')
        for (prefix, uri) in namespaces.items():
            if prefix:
                self.attribute(namespaceUri, tagName, 'xmlns:' + prefix, uri)
            else:
                self.attribute(namespaceUri, tagName, 'xmlns', uri)

        for (name, value) in attributes.items():
            self.attribute(namespaceUri, tagName, name, value)

        return

    def endElement(self, namespaceUri, tagName):
        """
        Handles an endElement event.

        Writes the closing tag for an element to the stream, or, if the
        element had no content, finishes writing the empty element tag.

        The namespaceUri argument is ignored in this class.
        """
        if self._inElement:
            self.writeAscii('/>')
            self._inElement = False
        else:
            self.writeAscii('</')
            self.writeEncode(tagName, 'end-tag name')
            self.writeAscii('>')
        return

    def attribute(self, elementUri, elementName, name, value):
        """
        Handles an attribute event.

        Writes an attribute to the stream as a space followed by
        the name, '=', and quote-delimited value. It is the caller's
        responsibility to ensure that this is called in the correct
        context, if well-formed output is desired.

        Preference is given to quotes (") around attribute values, in
        accordance with the DomWriter interface in DOM Level 3 Load and
        Save (25 July 2002 WD), although a value that contains quotes
        but no apostrophes will be delimited by apostrophes (') instead.
        The elementName arguments are not used by default,
        but may be used by subclasses.
        """
        self.writeAscii(' ')
        self.writeEncode(name, 'attribute name')
        self.writeAscii('=')
        if '"' in value and "'" not in value:
            entitymap = self.attrEntitiesApos
            quote = "'"
        else:
            entitymap = self.attrEntitiesQuot
            quote = '"'
        self.writeAscii(quote)
        self.writeEscape(value, entitymap)
        self.writeAscii(quote)
        return

    def text(self, text, disableEscaping=0):
        """
        Handles a text event.

        Writes character data to the stream. If the disableEscaping flag
        is not set, then unencodable characters are replaced with
        numeric character references; "&" and "<" are escaped as "&amp;"
        and "&lt;"; and ">" is escaped as "&gt;" if it is preceded by
        "]]". If the disableEscaping flag is set, then the characters
        are written to the stream with no escaping of any kind, which
        will result in an exception if there are unencodable characters.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        if disableEscaping:
            self.writeEncode(text, 'text')
        else:
            self.writeEscape(text, self.textEntities)
        return

    def cdataSection(self, data):
        """
        Handles a cdataSection event.

        Writes character data to the stream as a CDATA section.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        sections = data.split(']]>')
        self.writeAscii('<![CDATA[')
        self.writeEncode(sections[0], 'CDATA section')
        for section in sections[1:]:
            self.writeAscii(']]]]><![CDATA[>')
            self.writeEncode(section, 'CDATA section')

        self.writeAscii(']]>')
        return

    def processingInstruction(self, target, data):
        """
        Handles a processingInstruction event.

        Writes a processing instruction to the stream.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self.writeAscii('<?')
        self.writeEncode(target, 'processing instruction target')
        if data:
            self.writeAscii(' ')
            self.writeEncode(data, 'processing instruction data')
        self.writeAscii('?>')
        return

    def comment(self, data):
        """
        Handles a comment event.

        Writes a comment to the stream.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self.writeAscii('<!--')
        self.writeEncode(data, 'comment')
        self.writeAscii('-->')
        return

    textEntities = cStreamWriter.EntityMap({'<': '&lt;', '>': '&gt;', '&': '&amp;', '\r': '&#13;'})
    attrEntitiesQuot = cStreamWriter.EntityMap({'<': '&lt;', '&': '&amp;', '\t': '&#9;', '\n': '&#10;', '\r': '&#13;', '"': '&quot;'})
    attrEntitiesApos = cStreamWriter.EntityMap({'<': '&lt;', '&': '&amp;', '\t': '&#9;', '\n': '&#10;', '\r': '&#13;', "'": '&apos;'})


import re
from Ft.Xml import SplitQName
from Ft.Xml import XMLNS_NAMESPACE

class CanonicalXmlPrinter(XmlPrinter):
    """
    CanonicalXmlPrinter emits only c14n XML.
    http://www.ibm.com/developerworks/xml/library/x-c14n/
    http://www.w3.org/TR/xml-c14n
    Does not yet:
    * Normalize all attribute values
    * Specify all default attributes
    Note: this class is fully compatible with exclusive c14n:
    http://www.w3.org/TR/xml-exc-c14n/
    whether or not the operation is exclusive depends on preprocessing
    operations appplied by the caller.  See Ft.Xml.Lib.Print, for example
    """
    __module__ = __name__
    textEntities = cStreamWriter.EntityMap({'<': '&lt;', '>': '&gt;', '&': '&amp;', '\r': '&#xD;'})
    attrEntitiesQuot = cStreamWriter.EntityMap({'<': '&lt;', '&': '&amp;', '\t': '&#x9;', '\n': '&#xA;', '\r': '&#xD;', '"': '&quot;'})
    attrEntitiesApos = cStreamWriter.EntityMap({'<': '&lt;', '&': '&amp;', '\t': '&#x9;', '\n': '&#xA;', '\r': '&#xD;', "'": '&apos;'})
    attrNormPattern = re.compile('( |&#32;|&#x20;)+')

    def __init__(self, stream, encoding=None):
        __doc__ = XmlPrinter.__init__.__doc__
        __doc__ += '\n        Warning: the encoding parameter is ignored\n        '
        XmlPrinter.__init__(self, stream, 'UTF-8')
        self.reset()
        return

    def reset(self):
        """Sets the writer state as if it were a brand new instance"""
        self._ns_stack = [{None: '', 'xml': XMLNS_NAMESPACE}]
        XmlPrinter.reset(self)
        return
        return

    def startDocument(self, version='1.0', standalone=None):
        """
        No XML declaration is generated
        """
        self._ns_stack = [{None: '', 'xml': XMLNS_NAMESPACE}]
        return
        return

    def endDocument(self):
        """
        Writes any necessary final output to the stream.
        """
        if self._inElement:
            self.writeAscii('</')
            self.writeEncode(tagName, 'end-tag name')
            self.writeAscii('>')
        return

    def doctype(self, name, publicId, systemId):
        """
        Handles a doctype event.  No output in c14n.
        """
        return

    def startElement(self, namespaceUri, tagName, namespaces, attributes):
        """
        Handles a startElement event.

        Writes part of an element's start-tag or empty-element tag to
        the stream, and closes the start tag of the previous element,
        if one remained open. Writes the xmlns attributes for the given
        dictionary of namespaces, and invokes attribute() as neeeded to
        write the given dictionary of attributes.

        The namespaceUri argument is ignored in this class.
        """
        if self._inElement:
            self.writeAscii('>')
        else:
            self._inElement = True
        self.writeAscii('<')
        self.writeEncode(tagName, 'start-tag name')
        prefixes = namespaces.items()
        prefixes.sort()
        parent_prefixes = self._ns_stack[(-1)].items()
        for (prefix, uri) in prefixes:
            if (prefix, uri) not in parent_prefixes:
                if prefix:
                    self.attribute(namespaceUri, tagName, 'xmlns:' + prefix, uri)
                else:
                    self.attribute(namespaceUri, tagName, 'xmlns', uri)

        self._ns_stack.append(self._ns_stack[(-1)].copy())
        self._ns_stack[(-1)].update(namespaces)
        attrs = attributes.items()
        attrs = [ (self._ns_stack[(-1)].get(SplitQName(name)[0], None), name, value) for (name, value) in attributes.items() ]
        attrs.sort()
        for (ns, name, value) in attrs:
            self.attribute(namespaceUri, tagName, name, value)

        return
        return

    def endElement(self, namespaceUri, tagName):
        """
        Handles an endElement event.

        Writes the closing tag for an element to the stream.
        The namespaceUri argument is ignored in this class.
        """
        del self._ns_stack[-1]
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self.writeAscii('</')
        self.writeEncode(tagName, 'end-tag name')
        self.writeAscii('>')
        return

    def attribute(self, elementUri, elementName, name, value):
        """
        Handles an attribute event.

        Writes an attribute to the stream as a space followed by
        the name, '=', and quote-delimited value. It is the caller's
        responsibility to ensure that this is called in the correct
        context, if well-formed output is desired.

        The delimiter is always a quote ("), as required by c14n
        The elementName arguments are not used by default,
        but may be used by subclasses.
        """
        self.writeAscii(' ')
        self.writeEncode(name, 'attribute name')
        self.writeAscii('=')
        entitymap = self.attrEntitiesQuot
        quote = '"'
        self.writeAscii(quote)
        self.writeEscape(value, entitymap)
        self.writeAscii(quote)
        return

    def text(self, text, disableEscaping=0):
        """
        Handles a text event.

        Writes character data to the stream.  All characters should be
        suitable for encoding (UTF-8 only); "&" and "<" are escaped as "&amp;"
        and "&lt;"; and ">" is escaped as "&gt;" if it is preceded by
        "]]".

        disableEscaping is ignored.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        text.replace('\r\n', '\r')
        self.writeEscape(text, self.textEntities)
        return

    def cdataSection(self, data):
        """
        Handles a cdataSection event.

        No CDATA sections in c14n, so just commute to the text event
        """
        self.text(data)
        return

    def processingInstruction(self, target, data):
        """
        Handles a processingInstruction event.

        Writes a processing instruction to the stream.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self.writeAscii('<?')
        self.writeEncode(target, 'processing instruction target')
        if data:
            self.writeAscii(' ')
            self.writeEncode(data, 'processing instruction data')
        self.writeAscii('?>')
        return

    def comment(self, data):
        """
        Handles a comment event.

        Writes a comment to the stream.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self.writeAscii('<!--')
        self.writeEncode(data, 'comment')
        self.writeAscii('-->')
        return