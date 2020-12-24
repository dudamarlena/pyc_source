# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/converter.py
# Compiled at: 2019-05-21 05:08:42
from esdrt.content import MessageFactory as _
from z3c.form.converter import NumberDataConverter
from z3c.form.interfaces import IWidget
import zope
symbols = {'decimal': ',', 
   'group': '', 
   'list': ';', 
   'percentSign': '%', 
   'nativeZeroDigit': '0', 
   'patternDigit': '#', 
   'plusSign': '+', 
   'minusSign': '-', 
   'exponential': 'E', 
   'perMille': 'â\x88\x9e', 
   'infinity': 'ï¿½', 
   'nan': ''}

class ESDRTNumberDataConverter(NumberDataConverter):

    def __init__(self, field, widget):
        super(ESDRTNumberDataConverter, self).__init__(field, widget)
        self.formatter.symbols.update(symbols)


class ESDRTIntegerDataConverter(ESDRTNumberDataConverter):
    """A data converter for integers."""
    zope.component.adapts(zope.schema.interfaces.IInt, IWidget)
    type = int
    errorMessage = _('The entered value is not a valid integer literal.')