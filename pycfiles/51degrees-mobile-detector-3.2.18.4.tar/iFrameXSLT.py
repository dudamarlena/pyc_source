# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\iFrameXSLT.py
# Compiled at: 2005-09-19 16:44:10
__doc__ = '\nThe contents of this file are subject to the Mozilla Public License  \nVersion 1.1 (the "License"); you may not use this file except in  \ncompliance with the License. \nYou may obtain a copy of the License at http://www.mozilla.org/MPL/ \nSoftware distributed under the License is distributed on an "AS IS"  \nbasis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the  \nLicense for the specific language governing rights and limitations under  \nthe License. \n\nThe Original Code is available at \nhttp://downloads.xmlschemata.org/python/xvif/\n\nThe Initial Developer of the Original Code is Eric van der Vlist. Portions  \ncreated by Eric van der Vlist are Copyright (C) 2002. All Rights Reserved. \n\nContributor(s): \n'

def transform(self, node):
    from Ft.Xml.Xslt import Processor, StylesheetReader, DomWriter
    from Ft.Xml import InputSource
    processor = Processor.Processor()
    xreader = StylesheetReader.StylesheetReader()
    style = xreader.fromDocument(self.applyElt.dom, baseUri='dummy')
    processor.appendStylesheetInstance(style)
    factory = InputSource.DefaultFactory
    isrc = factory.fromString('dummy', 'dummy')
    resWriter = DomWriter.DomWriter()
    processor.execute(node, isrc, ignorePis=1, writer=resWriter)
    dom = resWriter.getResult()
    return dom.firstChild