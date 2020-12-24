# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\MessageElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the XSLT Spec import stylesheet element.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
import cStringIO
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo
from Ft.Xml.Xslt import OutputParameters, XmlWriter

class MessageElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {'terminate': AttributeInfo.YesNo(default='no')}

    def instantiate(self, context, processor):
        op = OutputParameters.OutputParameters()
        op.method = 'xml'
        op.encoding = processor.writers[(-1)]._outputParams.encoding
        op.omitXmlDeclaration = 1
        stream = cStringIO.StringIO()
        processor.pushResult(XmlWriter.XmlWriter(op, stream))
        try:
            for child in self.children:
                child.instantiate(context, processor)

        finally:
            processor.popResult()
        msg = stream.getvalue()
        if self._terminate:
            raise XsltRuntimeException(Error.STYLESHEET_REQUESTED_TERMINATION, self, msg)
        else:
            processor.xslMessage(msg)
        return