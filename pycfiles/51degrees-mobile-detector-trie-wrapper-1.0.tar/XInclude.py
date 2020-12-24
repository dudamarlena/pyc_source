# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XInclude.py
# Compiled at: 2005-04-12 01:33:33
__doc__ = '\nXInclude processing\n\nXInclude processing is normally controlled via the Domlette reader APIs\nand is implemented within Domlette itself. This module just provides\nconstants and classes to support XInclude processing.\n\nXInclude is defined at http://www.w3.org/TR/xinclude\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
__all__ = [
 'XINCLUDE_NAMESPACE', 'NONNORMATIVE_SCHEMA_FOR_XINCLUDE_ELEMENT', 'g_errorMessages']
XINCLUDE_NAMESPACE = 'http://www.w3.org/2001/XInclude'
NONNORMATIVE_SCHEMA_FOR_XINCLUDE_ELEMENT = '<?xml version="1.0" encoding="utf-8"?>\n<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"\n           xmlns:xi="http://www.w3.org/2001/XInclude"\n           targetNamespace="http://www.w3.org/2001/XInclude"\n           finalDefault="extension">\n\n  <xs:element name="include" type="xi:includeType" />\n\n  <xs:complexType name="includeType" mixed="true">\n    <xs:choice minOccurs=\'0\' maxOccurs=\'unbounded\' >\n      <xs:element ref=\'xi:fallback\' />\n      <xs:any namespace=\'##other\' processContents=\'lax\' />\n      <xs:any namespace=\'##local\' processContents=\'lax\' />\n    </xs:choice>\n    <xs:attribute name="href" use="optional" type="xs:anyURI"/>\n    <xs:attribute name="parse" use="optional" default="xml"\n                  type="xi:parseType" />\n    <xs:attribute name="xpointer" use="optional" type="xs:string"/>\n    <xs:attribute name="encoding" use="optional" type="xs:string"/>\n    <xs:attribute name="accept" use="optional" type="xs:string"/>\n    <xs:attribute name="accept-language" use="optional" type="xs:string"/>\n    <xs:anyAttribute namespace="##other" processContents="lax"/>\n  </xs:complexType>\n\n  <xs:simpleType name="parseType">\n    <xs:restriction base="xs:token">\n      <xs:enumeration value="xml"/>\n      <xs:enumeration value="text"/>\n    </xs:restriction>\n  </xs:simpleType>\n\n  <xs:element name="fallback" type="xi:fallbackType" />\n\n  <xs:complexType name="fallbackType" mixed="true">\n    <xs:choice minOccurs="0" maxOccurs="unbounded">\n      <xs:element ref="xi:include"/>\n      <xs:any namespace="##other" processContents="lax"/>\n      <xs:any namespace="##local" processContents="lax"/>\n    </xs:choice>\n    <xs:anyAttribute namespace="##other" processContents="lax" />\n  </xs:complexType>\n\n</xs:schema>'
import warnings

def ProcessIncludesFromUri(uri, validate=0):
    """
    DEPRECATED - The Ft.Xml.Domlette readers expand XIncludes by default.
    """
    warnings.warn('ProcessIncludesFromUri() is deprecated', DeprecationWarning, 2)
    if validate:
        from Ft.Xml.Domlette import ValidatingReader as reader
    else:
        from Ft.Xml.Domlette import NonvalidatingReader as reader
    return reader.parseUri(uri)


def ProcessIncludesFromString(string, uri='', validate=0):
    """
    DEPRECATED - The Ft.Xml.Domlette readers expand XIncludes by default.
    """
    warnings.warn('ProcessIncludesFromString() is deprecated', DeprecationWarning, 2)
    if validate:
        from Ft.Xml.Domlette import ValidatingReader as reader
    else:
        from Ft.Xml.Domlette import NonvalidatingReader as reader
    return reader.parseString(string, uri)


def ProcessIncludesFromSource(inputSource, validate=0):
    """
    DEPRECATED - The Ft.Xml.Domlette readers expand XIncludes by default.
    """
    warnings.warn('ProcessIncludesFromSource() is deprecated', DeprecationWarning, 2)
    if validate:
        from Ft.Xml.Domlette import ValidatingReader as reader
    else:
        from Ft.Xml.Domlette import NonvalidatingReader as reader
    return reader.parse(inputSource)