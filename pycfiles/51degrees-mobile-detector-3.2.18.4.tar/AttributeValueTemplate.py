# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\AttributeValueTemplate.py
# Compiled at: 2006-08-17 09:53:54
__doc__ = '\nImplementation of XSLT attribute value templates\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml.Xslt import XsltException, Error
from Ft.Xml.XPath import Conversions
import AvtParserc
_AvtParser = AvtParserc.AvtParser()
del AvtParserc

class AttributeValueTemplate:
    __module__ = __name__

    def __init__(self, source, validator=None, element=None):
        self.source = source
        self.validator = validator
        self.element = element
        try:
            parts = _AvtParser.parse(source)
        except SyntaxError, exc:
            raise XsltException(Error.AVT_SYNTAX)

        self._resultFormat = ''
        self._parsedParts = parsed_parts = []
        for part in parts:
            if isinstance(part, unicode):
                if '%' in part:
                    part = part.replace('%', '%%')
                self._resultFormat += part
            else:
                self._resultFormat += '%s'
                parsed_parts.append(part)

        return

    def isConstant(self):
        return not self._parsedParts

    def evaluate(self, context):
        if not self.element and hasattr(context, 'currentInstruction'):
            self.element = context.currentInstruction
        convert = Conversions.StringValue
        result = self._resultFormat % tuple([ convert(x.evaluate(context)) for x in self._parsedParts ])
        if self.validator:
            return self.validator.reprocess(self.element, result)
        else:
            return result

    def __nonzero__(self):
        return self.source is not None
        return