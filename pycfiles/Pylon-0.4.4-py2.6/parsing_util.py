# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\io\parsing_util.py
# Compiled at: 2010-12-26 13:36:33
""" Defines convenience pyparsing constructs and token converters.

Based on sparser.py by Tim Cera timcera@earthlink.net.
"""
from pyparsing import TokenConverter, oneOf, string, Literal, Group, Word, Optional, Combine, sglQuotedString, dblQuotedString, restOfLine, nums

class ToBoolean(TokenConverter):
    """ Converter to make token boolean """

    def postParse(self, instring, loc, tokenlist):
        """ Converts the first token to boolean """
        return bool(tokenlist[0])


class ToInteger(TokenConverter):
    """ Converter to make token into an integer """

    def postParse(self, instring, loc, tokenlist):
        """ Converts the first token to an integer """
        return int(tokenlist[0])


class ToFloat(TokenConverter):
    """ Converter to make token into a float """

    def postParse(self, instring, loc, tokenlist):
        """ Converts the first token into a float """
        return float(tokenlist[0])


decimal_sep = '.'
sign = oneOf('+ -')
scolon = Literal(';').suppress()
matlab_comment = Group(Literal('%') + restOfLine).suppress()
psse_comment = Literal('@!') + Optional(restOfLine)
special_chars = string.replace('!"#$%&\'()*,./:;<=>?@[\\]^_`{|}~', decimal_sep, '')
boolean = ToBoolean(ToInteger(Word('01', exact=1))).setName('bool')
integer = ToInteger(Combine(Optional(sign) + Word(nums))).setName('integer')
positive_integer = ToInteger(Combine(Optional('+') + Word(nums))).setName('integer')
negative_integer = ToInteger(Combine('-' + Word(nums))).setName('integer')
real = ToFloat(Combine(Optional(sign) + Word(nums) + Optional(decimal_sep + Word(nums)) + Optional(oneOf('E e') + Optional(sign) + Word(nums)))).setName('real')
positive_real = ToFloat(Combine(Optional('+') + Word(nums) + decimal_sep + Optional(Word(nums)) + Optional(oneOf('E e') + Word(nums)))).setName('real')
negative_real = ToFloat(Combine('-' + Word(nums) + decimal_sep + Optional(Word(nums)) + Optional(oneOf('E e') + Word(nums)))).setName('real')
q_string = (sglQuotedString | dblQuotedString).setName('q_string')
colon = Literal(':')
lbrace = Literal('{')
rbrace = Literal('}')
lbrack = Literal('[')
rbrack = Literal(']')
lparen = Literal('(')
rparen = Literal(')')
equals = Literal('=')
comma = Literal(',')
dot = Literal('.')
slash = Literal('/')
bslash = Literal('\\')
star = Literal('*')
semi = Literal(';')
at = Literal('@')
minus = Literal('-')
comma_sep = comma.suppress()

def make_unique_name(base, existing=[], format='%s_%s'):
    """ Return a name, unique within a context, based on the specified name.

    @param base: the desired base name of the generated unique name.
    @param existing: a sequence of the existing names to avoid returning.
    @param format: a formatting specification for how the name is made unique.
    """
    count = 2
    name = base
    while name in existing:
        name = format % (base, count)
        count += 1

    return name