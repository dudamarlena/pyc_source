# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/_edit_descriptors.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 8498 bytes
from ._exceptions import *

def get_edit_descriptor_obj(name):
    """Returns a new object instance from a string"""
    name = name.upper()
    if name == 'A':
        return A()
    if name == 'B':
        return B()
    if name == 'BN':
        return BN()
    if name == 'BZ':
        return BZ()
    if name == ':':
        return Colon()
    if name == 'D':
        return D()
    if name == 'E':
        return E()
    if name == 'EN':
        return EN()
    if name == 'ES':
        return ES()
    if name == 'F':
        return F()
    if name == 'G':
        return G()
    if name == 'H':
        return H()
    if name == 'I':
        return I()
    if name == 'L':
        return L()
    if name == 'O':
        return O()
    if name == 'P':
        return P()
    if name == 'S':
        return S()
    if name == '/':
        return Slash()
    if name == 'SP':
        return SP()
    if name == 'SS':
        return SS()
    if name == 'T':
        return T()
    if name == 'TL':
        return TL()
    if name == 'TR':
        return TR()
    if name == 'X':
        return X()
    if name == 'Z':
        return Z()
    raise InvalidFormat('Expected an edit descriptor, got %s' % name)


class A(object):

    def __init__(self):
        self.repeat = None
        self.width = None

    def __repr__(self):
        return '<A repeat=' + str(self.repeat) + ' width=' + str(self.width) + '>'


class QuotedString(object):

    def __init__(self, char_string=None):
        self.char_string = char_string

    def get_width(self):
        return len(self.char_string)

    width = property(get_width)

    def __repr__(self):
        return '<QuotedString char_string=' + str(self.char_string) + '>'


class B(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.min_digits = None

    def __repr__(self):
        return '<B repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' min_digits=' + str(self.min_digits) + '>'


class BN(object):

    def __init__(self):
        pass

    def __repr__(self):
        return '<BN>'


class BZ(object):

    def __init__(self):
        pass

    def __repr__(self):
        return '<BZ>'


class Colon(object):

    def __init__(self):
        pass

    def __repr__(self):
        return '<Colon>'


class D(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.decimal_places = None

    def __repr__(self):
        return '<D repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' decimal_places=' + str(self.decimal_places) + '>'


class E(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.decimal_places = None
        self.exponent = None

    def __repr__(self):
        return '<E repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' decimal_places=' + str(self.decimal_places) + ' exponent=' + str(self.exponent) + '>'


class EN(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.decimal_places = None
        self.exponent = None

    def __repr__(self):
        return '<EN repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' decimal_places=' + str(self.decimal_places) + ' exponent=' + str(self.exponent) + '>'


class ES(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.decimal_places = None
        self.exponent = None

    def __repr__(self):
        return '<ES repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' decimal_places=' + str(self.decimal_places) + ' exponent=' + str(self.exponent) + '>'


class F(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.decimal_places = None

    def __repr__(self):
        return '<F repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' decimal_places=' + str(self.decimal_places) + '>'


class FormatGroup(object):
    pass


class G(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.decimal_places = None
        self.exponent = None

    def __repr__(self):
        return '<G repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' decimal_places=' + str(self.decimal_places) + ' exponent=' + str(self.exponent) + '>'


class H(object):

    def __init__(self):
        self.num_chars = None
        self.char_string = None

    def __repr__(self):
        return '<H num_chars=' + str(self.num_chars) + ' char_string=' + str(self.char_string) + '>'


class I(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.min_digits = None

    def __repr__(self):
        return '<I repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' min_digits=' + str(self.min_digits) + '>'


class L(object):

    def __init__(self):
        self.repeat = None
        self.width = None

    def __repr__(self):
        return '<L repeat=' + str(self.repeat) + ' width=' + str(self.width) + '>'


class O(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.min_digits = None

    def __repr__(self):
        return '<O repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' min_digits=' + str(self.min_digits) + '>'


class P(object):

    def __init__(self):
        self.scale = None

    def __repr__(self):
        return '<P scale=' + str(self.scale) + '>'


class S(object):

    def __init__(self):
        pass

    def __repr__(self):
        return '<S>'


class Slash(object):

    def __init__(self):
        self.repeat = None

    def __repr__(self):
        return '<Slash repeat=' + str(self.repeat) + '>'


class SP(object):

    def __init__(self):
        pass

    def __repr__(self):
        return '<SP>'


class SS(object):

    def __init__(self):
        pass

    def __repr__(self):
        return '<SS>'


class T(object):

    def __init__(self):
        self.num_chars = None

    def __repr__(self):
        return '<T num_chars=' + str(self.num_chars) + '>'


class TL(object):

    def __init__(self):
        self.num_chars = None

    def __repr__(self):
        return '<TL num_chars=' + str(self.num_chars) + '>'


class TR(object):

    def __init__(self):
        self.num_chars = None

    def __repr__(self):
        return '<TR num_chars=' + str(self.num_chars) + '>'


class X(object):

    def __init__(self):
        self.num_chars = None

    def __repr__(self):
        return '<X num_chars=' + str(self.num_chars) + '>'


class Z(object):

    def __init__(self):
        self.repeat = None
        self.width = None
        self.min_digits = None

    def __repr__(self):
        return '<Z repeat=' + str(self.repeat) + ' width=' + str(self.width) + ' min_digits=' + str(self.min_digits) + '>'


ED1 = [
 'BN', 'BZ', 'SP', 'SS', 'S']
ED2 = ['X']
ED3 = ['T', 'TR', 'TL', 'L']
ED4 = ['A']
ED5 = ['D', 'F']
ED6 = ['B', 'I', 'O', 'Z']
ED7 = ['E', 'EN', 'ES', 'G']
ED8 = ['P']
ED9 = [':']
ED10 = ['/']
REPEATABLE_EDS = ['L', 'A', 'D', 'F', 'B', 'I', 'O', 'Z', 'E', 'EN', 'ES', 'G', '/']
OUTPUT_EDS = (L, A, D, F, B, I, O, Z, E, EN, ES, G)
CONTROL_EDS = (BN, BZ, P, SP, SS, S, X, T, TR, TL, Colon, Slash)
NON_REVERSION_EDS = (P, S, SP, SS, BN, BZ)
ALL_ED = ED1 + ED2 + ED3 + ED4 + ED5 + ED6 + ED7 + ED8 + ED9 + ED10