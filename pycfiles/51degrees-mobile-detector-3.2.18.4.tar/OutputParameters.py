# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\OutputParameters.py
# Compiled at: 2005-10-19 10:02:59
__doc__ = '\nRepresents XSLT output parameters governed by the xsl:output instruction\nSee also Ft.Xml.Xslt.OutputHandler\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml.Xslt.AttributeValueTemplate import AttributeValueTemplate
from Ft.Xml.XPath import FT_EXT_NAMESPACE

class OutputParameters:
    __module__ = __name__

    def __init__(self):
        self.method = None
        self.version = None
        self.encoding = None
        self.omitXmlDeclaration = None
        self.standalone = None
        self.doctypeSystem = None
        self.doctypePublic = None
        self.mediaType = None
        self.cdataSectionElements = []
        self.indent = None
        self.utfbom = None
        return

    def clone(self):
        clone = OutputParameters()
        clone.__dict__.update(self.__dict__)
        return clone

    def setDefault(self, attr, value):
        if not self.__dict__.has_key(attr):
            raise AttributeError(attr)
        if self.__dict__[attr] is None:
            self.__dict__[attr] = value
        return
        return

    def avtParse(self, owner, context):
        """
        evaluates the given node for valid xsl:output-like attributes
        expressed in AVTs of extension elements, storing the values
        in instance variables.  If called repeatedly, it will overwrite
        old values.
        """
        method = owner._method.evaluate(context)
        if method is not None:
            self.method = method
        version = owner._version.evaluate(context)
        if version is not None:
            self.version = version
        encoding = owner._encoding.evaluate(context)
        if encoding is not None:
            self.encoding = encoding
        omit_xml_decl = owner._omit_xml_declaration.evaluate(context)
        if omit_xml_decl is not None:
            self.omitXmlDeclaration = omit_xml_decl
        standalone = owner._standalone.evaluate(context)
        if standalone is not None:
            self.standalone = standalone and 'yes' or 'no'
        doctype_system = owner._doctype_system.evaluate(context)
        if doctype_system is not None:
            self.doctypeSystem = doctype_system
        doctype_public = owner._doctype_public.evaluate(context)
        if doctype_public is not None:
            self.doctypePublic = doctype_public
        media_type = owner._media_type.evaluate(context)
        if media_type is not None:
            self.mediaType = media_type
        self.cdataSectionElements.extend(owner._cdata_section_elements.evaluate(context))
        indent = owner._indent.evaluate(context)
        if indent is not None:
            self.indent = indent
        if owner.attributes.has_key((FT_EXT_NAMESPACE, 'utf-bom')):
            utfbom = owner.attributes[(FT_EXT_NAMESPACE, 'utf-bom')].evaluate(context)
            if utfbom is not None:
                self.utfbom = utfbom
        return
        return

    def parse(self, owner):
        """
        parses the given node (owner) for valid xsl:output attributes
        and stores their values in instance variables.
        If called repeatedly, it will overwrite old values (this ensures
        behavior mandated by the spec, in which the last xsl:output element
        is established with highest precedence).
        """
        if owner._method is not None:
            self.method = owner._method
        if owner._version is not None:
            self.version = owner._version
        if owner._encoding is not None:
            self.encoding = owner._encoding
        if owner._omit_xml_declaration is not None:
            self.omitXmlDeclaration = owner._omit_xml_declaration
        if owner._standalone is not None:
            self.standalone = owner._standalone and 'yes' or 'no'
        if owner._doctype_system is not None:
            self.doctypeSystem = owner._doctype_system
        if owner._doctype_public is not None:
            self.doctypePublic = owner._doctype_public
        if owner._media_type is not None:
            self.mediaType = owner._media_type
        self.cdataSectionElements.extend(owner._cdata_section_elements)
        if owner._indent is not None:
            self.indent = owner._indent
        if owner.attributes.has_key((FT_EXT_NAMESPACE, 'utf-bom')):
            self.utfbom = owner.attributes[(FT_EXT_NAMESPACE, 'utf-bom')]
        return
        return