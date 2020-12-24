# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\MessageElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec import stylesheet element.\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
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