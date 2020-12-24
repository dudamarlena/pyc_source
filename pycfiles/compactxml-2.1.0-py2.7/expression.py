# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compactxml/expression.py
# Compiled at: 2010-10-25 15:54:18
from __future__ import absolute_import
import re, copy
from lxml import etree
import pyparsing
from .error import ExpandError
xmlName = pyparsing.Regex('[_\\w][-_.\\w]*', re.U)('name')
prefix = xmlName('prefix')
prefixedName = pyparsing.Optional(prefix + pyparsing.Literal(':').suppress()) + xmlName
aDefaultNamespaces = {'xml': 'http://www.w3.org/XML/1998/namespace', 
   'xmlns': 'http://www.w3.org/2000/xmlns'}

class Expression(object):

    def __init__--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             1  'aParts'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               2
               12  BINARY_MODULO    
               13  LOAD_CONST               0
               16  COMPARE_OP            2  ==
               19  POP_JUMP_IF_TRUE     31  'to 31'
               22  LOAD_ASSERT              AssertionError
               25  LOAD_CONST               'All expression parts must have an operator and value.'
               28  RAISE_VARARGS_2       2  None

 L.  24        31  LOAD_FAST             1  'aParts'
               34  LOAD_FAST             0  'self'
               37  STORE_ATTR            2  'aParts'

 L.  25        40  LOAD_FAST             2  'aNamespaces'
               43  LOAD_FAST             0  'self'
               46  STORE_ATTR            3  'aNamespaces'

 L.  26        49  LOAD_FAST             3  'aVariables'
               52  LOAD_FAST             0  'self'
               55  STORE_ATTR            4  'aVariables'

Parse error at or near `LOAD_FAST' instruction at offset 52

    def __iter__(self):
        aParts = copy.copy(self.aParts.asList())
        aParts.reverse()
        while True:
            try:
                operator = aParts.pop()
                value = aParts.pop()
            except IndexError:
                break

            yield (
             operator, value)

    def value(self):
        combined = ''
        for operator, value in self:
            if operator == '+':
                combined += value
            elif operator == '\\':
                combined += '\n'
                combined += value
            elif operator == '$':
                combined += self.aVariables.lookup(value)

        return combined

    def parse_prefixed_name(self, unparsed):
        try:
            return prefixedName.parseString(unparsed, True)
        except pyparsing.ParseException as exception:
            error = ExpandError('Error parsing name in expression: ' + exception.msg)
            raise error

    def parse_prefix(self, unparsed):
        try:
            return prefix.parseString(unparsed, True)
        except pyparsing.ParseException as exception:
            error = ExpandError('Error parsing prefix in expression: ' + exception.msg)
            raise error

    def name(self):
        parsed = self.parse_prefixed_name(self.value())
        name = parsed['name']
        try:
            prefix = parsed['prefix']
        except KeyError:
            return name

        return prefix + ':' + name

    def qname(self):
        global aDefaultNamespaces
        parsed = self.parse_prefixed_name(self.value())
        name = parsed['name']
        try:
            prefix = parsed['prefix']
        except KeyError:
            try:
                namespace = self.aNamespaces[None]
            except KeyError:
                return etree.QName(name)

        else:
            try:
                namespace = aDefaultNamespaces[prefix]
            except KeyError:
                namespace = self.aNamespaces[prefix]

        if namespace:
            return etree.QName(namespace, name)
        else:
            return etree.QName(name)
            return

    def prefix(self):
        parsed = self.parse_prefix(self.value())
        parsedPrefix = parsed['prefix']
        return parsedPrefix

    def attribute(self):
        parsed = self.parse_prefixed_name(self.value())
        name = parsed['name']
        try:
            prefix = parsed['prefix']
        except KeyError:
            return etree.QName(name)

        try:
            namespace = aDefaultNamespaces[prefix]
        except KeyError:
            namespace = self.aNamespaces[prefix]

        if namespace:
            return etree.QName(namespace, name)
        else:
            return etree.QName(name)

    @staticmethod
    def build(command, value, aVariables):
        aaParts = []
        for eOperator, eValue in aVariables.partition(value):
            if eOperator == '+':
                for ePart in eValue.split('\n'):
                    aaParts.append((eOperator, ePart))
                    eOperator = '\\'

            else:
                aaParts.append((eOperator, eValue))

        if aaParts[0][0] == '+':
            aaParts[0] = (
             command, aaParts[0][1])
        else:
            aaParts.insert(0, (command, ''))

        def quote(value):
            if ' ' in value or '\t' in value or '"' in value:
                return '"%s"' % value.replace('"', '""')
            else:
                return value

        aaParts = map(lambda (eOperator, eValue): (eOperator, quote(eValue)), aaParts)
        aLines = map(lambda aParts: ('').join(aParts), aaParts)
        return aLines


class NamedExpression(object):

    def __init__--- This code section failed: ---

 L. 163         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             1  'aParts'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               0
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_FALSE    39  'to 39'

 L. 164        18  LOAD_CONST               None
               21  LOAD_FAST             0  'self'
               24  STORE_ATTR            2  'nameExpression'

 L. 165        27  LOAD_CONST               None
               30  LOAD_FAST             0  'self'
               33  STORE_ATTR            3  'valueExpression'
               36  JUMP_FORWARD        176  'to 215'

 L. 166        39  LOAD_GLOBAL           0  'len'
               42  LOAD_FAST             1  'aParts'
               45  CALL_FUNCTION_1       1  None
               48  LOAD_CONST               1
               51  COMPARE_OP            2  ==
               54  POP_JUMP_IF_FALSE    94  'to 94'

 L. 167        57  LOAD_GLOBAL           4  'Expression'
               60  LOAD_FAST             1  'aParts'
               63  LOAD_CONST               0
               66  BINARY_SUBSCR    
               67  LOAD_FAST             2  'aNamespaces'
               70  LOAD_FAST             3  'aVariables'
               73  CALL_FUNCTION_3       3  None
               76  LOAD_FAST             0  'self'
               79  STORE_ATTR            2  'nameExpression'

 L. 168        82  LOAD_CONST               None
               85  LOAD_FAST             0  'self'
               88  STORE_ATTR            3  'valueExpression'
               91  JUMP_FORWARD        121  'to 215'

 L. 169        94  LOAD_GLOBAL           0  'len'
               97  LOAD_FAST             1  'aParts'
              100  CALL_FUNCTION_1       1  None
              103  LOAD_CONST               3
              106  COMPARE_OP            2  ==
              109  POP_JUMP_IF_FALSE   190  'to 190'

 L. 170       112  LOAD_GLOBAL           4  'Expression'
              115  LOAD_FAST             1  'aParts'
              118  LOAD_CONST               0
              121  BINARY_SUBSCR    
              122  LOAD_FAST             2  'aNamespaces'
              125  LOAD_FAST             3  'aVariables'
              128  CALL_FUNCTION_3       3  None
              131  LOAD_FAST             0  'self'
              134  STORE_ATTR            2  'nameExpression'

 L. 171       137  LOAD_FAST             1  'aParts'
              140  LOAD_CONST               1
              143  BINARY_SUBSCR    
              144  LOAD_CONST               '='
              147  COMPARE_OP            2  ==
              150  POP_JUMP_IF_TRUE    162  'to 162'
              153  LOAD_ASSERT              AssertionError
              156  LOAD_CONST               'Named expression must contain equal sign.'
              159  RAISE_VARARGS_2       2  None

 L. 172       162  LOAD_GLOBAL           4  'Expression'
              165  LOAD_FAST             1  'aParts'
              168  LOAD_CONST               2
              171  BINARY_SUBSCR    
              172  LOAD_FAST             2  'aNamespaces'
              175  LOAD_FAST             3  'aVariables'
              178  CALL_FUNCTION_3       3  None
              181  LOAD_FAST             0  'self'
              184  STORE_ATTR            3  'valueExpression'
              187  JUMP_FORWARD         25  'to 215'

 L. 174       190  LOAD_GLOBAL           6  'False'
              193  POP_JUMP_IF_TRUE    215  'to 215'
              196  LOAD_ASSERT              AssertionError
              199  LOAD_CONST               'Wrong number of parts (%d) for named expression.'
              202  LOAD_GLOBAL           0  'len'
              205  LOAD_FAST             1  'aParts'
              208  CALL_FUNCTION_1       1  None
              211  BINARY_MODULO    
              212  RAISE_VARARGS_2       2  None
            215_0  COME_FROM           187  '187'
            215_1  COME_FROM            91  '91'
            215_2  COME_FROM            36  '36'
              215  LOAD_CONST               None
              218  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 215_0

    def value(self):
        if self.valueExpression is None:
            return
        else:
            return self.valueExpression.value()
            return

    def __parse_name(self, method):
        if self.nameExpression is None:
            return
        else:
            return getattr(self.nameExpression, method)()
            return

    def name(self):
        return self.__parse_name('name')

    def qname(self):
        return self.__parse_name('qname')

    def prefix(self):
        return self.__parse_name('prefix')

    def attribute(self):
        return self.__parse_name('attribute')

    @staticmethod
    def build(command, name, value, aVariables):
        aNameLines = Expression.build(command, name, aVariables)
        aValueLines = Expression.build('=', value, aVariables)
        aNameLines[-1] = aNameLines[(-1)] + aValueLines[0]
        aNameLines.extend(aValueLines[1:])
        return aNameLines