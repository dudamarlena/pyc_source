# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/etree.py
# Compiled at: 2012-08-15 03:48:07
import sys
PY3 = sys.version_info[0] > 2
import xml.etree.ElementTree as etree
CDATA_TPL = '<![CDATA[%s]]>'
CDATA_TAG = CDATA_TPL

def CDATA(text):
    element = etree.Element(CDATA_TAG)
    element.text = text
    return element


original_serialize_xml = etree._serialize_xml
if PY3:

    def _serialize_xml_with_CDATA_support(write, elem, qnames, namespaces):
        if elem.tag == CDATA_TAG:
            write(CDATA_TPL % elem.text)
        else:
            original_serialize_xml(write, elem, qnames, namespaces)


else:

    def _serialize_xml_with_CDATA_support(write, elem, encoding, qnames, namespaces):
        if elem.tag == CDATA_TAG:
            write(CDATA_TPL % elem.text.encode(encoding))
        else:
            original_serialize_xml(write, elem, encoding, qnames, namespaces)


etree._serialize_xml = _serialize_xml_with_CDATA_support