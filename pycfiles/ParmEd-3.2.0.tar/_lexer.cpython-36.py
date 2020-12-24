# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/_lexer.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 5743 bytes
from ._edit_descriptors import *
from ._exceptions import *
DIGITS = [
 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
SIGNS = ['+', '-']
COMMA = [',']
DOT = ['.']
WHITESPACE = [' ', '\t', '\n']
QUOTE_CHARS = ['"', "'"]
DOUBLE_EDIT_DESCRIPTORS = ['EN', 'ES', 'TR', 'TL', 'BN', 'BZ', 'SP', 'SS']
SINGLE_EDIT_DESCRIPTORS = ['A', 'B', 'D', 'E', 'F', 'G', 'I', 'L', 'O', 'P', 'S', 'T', 'X', 'Z', ':', '/']
H_EDIT_DESCRIPTOR = ['H']
LEFT_PARENS = ['(']
RIGHT_PARENS = [')']
COLON = ':'
SLASH = '/'

def lexer(format):
    """Lex the FORTRAN format statement into tokens"""
    tokens = []
    s = -1
    h_chars = None
    while True:
        s = s + 1
        c0, c1, c2 = _get_chars(format, s)
        if c0 is None:
            break
        elif h_chars is not None:
            buff = format[s:s + h_chars]
            tokens.append(Token('QUOTED_STRING', buff))
            s = s + (h_chars - 1)
            h_chars = None
        elif c0 in WHITESPACE:
            continue
        elif c0 in QUOTE_CHARS:
            buff = ''
            delim = c0
            while True:
                s = s + 1
                c0, c1, c2 = _get_chars(format, s)
                if c0 == delim:
                    if c1 == delim:
                        s = s + 1
                        buff = buff + delim
                if c0 == delim:
                    break
                else:
                    if c0 is None:
                        raise InvalidFormat('Premature end of quoted string in format')
                    else:
                        buff = buff + c0

            tokens.append(Token('QUOTED_STRING', buff))
        elif c0 in DIGITS + SIGNS:
            if c0 in SIGNS:
                if c1 not in DIGITS:
                    raise InvalidFormat("Orphaned sign '%s' with no digits at position %d" % (c0, s))
            else:
                buff = c0
                while 1:
                    s = s + 1
                    c0, c1, c2 = _get_chars(format, s)
                    if c0 not in DIGITS or c0 is None:
                        break
                    else:
                        buff = buff + c0

                s = s - 1
                val = int(buff)
                if buff[0] in SIGNS:
                    tokens.append(Token('INT', val))
                else:
                    if val == 0:
                        tokens.append(Token('UINT', val))
                    else:
                        tokens.append(Token('NZUINT', val))
        elif c0 in COMMA:
            tokens.append(Token('COMMA', None))
        elif c0 in DOT:
            tokens.append(Token('DOT', None))
        elif c1 is not None and (c0 + c1).upper() in DOUBLE_EDIT_DESCRIPTORS:
            ed_type = _get_ed_type((c0 + c1).upper())
            tokens.append(Token(ed_type, (c0 + c1).upper()))
            s = s + 1
        elif c0.upper() in H_EDIT_DESCRIPTOR:
            if len(tokens) > 0:
                if tokens[(-1)].type in ('NZUINT', 'UINT'):
                    h_chars = tokens[(-1)].value
                    tokens = tokens[:-1]
            else:
                raise InvalidFormat('Missing H descriptor number argument at position %d' % s)
        elif c0.upper() in SINGLE_EDIT_DESCRIPTORS:
            ed_type = _get_ed_type(c0.upper())
            tokens.append(Token(ed_type, c0.upper()))
        else:
            if c0 in LEFT_PARENS:
                tokens.append(Token('LEFT_PARENS', None))
            else:
                if c0 in RIGHT_PARENS:
                    tokens.append(Token('RIGHT_PARENS', None))
                else:
                    raise InvalidFormat('Character %s not recognised at position %d' % (c0, s))

    return tokens


def _get_ed_type(ed_string):
    if ed_string in ED1:
        ed_type = 'ED1'
    else:
        if ed_string in ED2:
            ed_type = 'ED2'
        else:
            if ed_string in ED3:
                ed_type = 'ED3'
            else:
                if ed_string in ED4:
                    ed_type = 'ED4'
                else:
                    if ed_string in ED5:
                        ed_type = 'ED5'
                    else:
                        if ed_string in ED6:
                            ed_type = 'ED6'
                        else:
                            if ed_string in ED7:
                                ed_type = 'ED7'
                            else:
                                if ed_string in ED8:
                                    ed_type = 'ED8'
                                else:
                                    if ed_string in ED9:
                                        ed_type = 'ED9'
                                    else:
                                        if ed_string in ED10:
                                            ed_type = 'ED10'
                                        else:
                                            ed_type = None
    return ed_type


def _get_chars(format, s):
    try:
        c0 = format[s]
    except IndexError:
        c0 = None

    try:
        c1 = format[(s + 1)]
    except IndexError:
        c1 = None

    try:
        c2 = format[(s + 2)]
    except IndexError:
        c2 = None

    return (
     c0, c1, c2)


class InvalidFormat(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '\n  Token: type=%s,\tvalue=%s' % (self.type, str(self.value))