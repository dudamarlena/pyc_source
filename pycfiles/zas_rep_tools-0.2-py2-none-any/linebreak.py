# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/linebreak.py
# Compiled at: 2018-07-23 18:20:27
"""Unicode line breaking algorithm

UAX #14: Unicode Line Breaking Algorithm
    http://www.unicode.org/reports/tr14/tr14-24.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from unicodedata import east_asian_width
from .breaking import boundaries, break_units
from .codepoint import ord, unichr, code_point, code_points
from .db import line_break as _line_break
__all__ = [
 b'line_break',
 b'line_break_breakables',
 b'line_break_boundaries',
 b'line_break_units']
BK = b'BK'
CR = b'CR'
LF = b'LF'
CM = b'CM'
NL = b'NL'
SG = b'SG'
WJ = b'WJ'
ZW = b'ZW'
GL = b'GL'
SP = b'SP'
B2 = b'B2'
BA = b'BA'
BB = b'BB'
HY = b'HY'
CB = b'CB'
CL = b'CL'
CP = b'CP'
EX = b'EX'
IN = b'IN'
NS = b'NS'
OP = b'OP'
QU = b'QU'
IS = b'IS'
NU = b'NU'
PO = b'PO'
PR = b'PR'
SY = b'SY'
AI = b'AI'
AL = b'AL'
CJ = b'CJ'
H2 = b'H2'
H3 = b'H3'
HL = b'HL'
ID = b'ID'
JL = b'JL'
JV = b'JV'
JT = b'JT'
RI = b'RI'
SA = b'SA'
XX = b'XX'
pair_table = {OP: {OP: b'^', CL: b'^', CP: b'^', QU: b'^', GL: b'^', NS: b'^', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'^', PO: b'^', NU: b'^', AL: b'^', 
        ID: b'^', IN: b'^', HY: b'^', BA: b'^', BB: b'^', B2: b'^', 
        ZW: b'^', CM: b'@', WJ: b'^', H2: b'^', H3: b'^', JL: b'^', 
        JV: b'^', JT: b'^', CB: b'^'}, 
   CL: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'^', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   CP: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'^', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'%', AL: b'%', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   QU: {OP: b'^', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'%', AL: b'%', 
        ID: b'%', IN: b'%', HY: b'%', BA: b'%', BB: b'%', B2: b'%', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'%', H3: b'%', JL: b'%', 
        JV: b'%', JT: b'%', CB: b'%'}, 
   GL: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'%', AL: b'%', 
        ID: b'%', IN: b'%', HY: b'%', BA: b'%', BB: b'%', B2: b'%', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'%', H3: b'%', JL: b'%', 
        JV: b'%', JT: b'%', CB: b'%'}, 
   NS: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   EX: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   SY: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   IS: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'%', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   PR: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'%', 
        ID: b'%', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'%', H3: b'%', JL: b'%', 
        JV: b'%', JT: b'%', CB: b'_'}, 
   PO: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'%', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   NU: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'%', AL: b'%', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   AL: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'%', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   ID: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   IN: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   HY: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'_', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   BA: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'_', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   BB: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'%', AL: b'%', 
        ID: b'%', IN: b'%', HY: b'%', BA: b'%', BB: b'%', B2: b'%', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'%', H3: b'%', JL: b'%', 
        JV: b'%', JT: b'%', CB: b'_'}, 
   B2: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'%', BA: b'%', BB: b'_', B2: b'^', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   ZW: {OP: b'_', CL: b'_', CP: b'_', QU: b'_', GL: b'_', NS: b'_', EX: b'_', 
        SY: b'_', IS: b'_', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'_', BA: b'_', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'_', WJ: b'_', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   CM: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'%', AL: b'%', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}, 
   WJ: {OP: b'%', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'%', PO: b'%', NU: b'%', AL: b'%', 
        ID: b'%', IN: b'%', HY: b'%', BA: b'%', BB: b'%', B2: b'%', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'%', H3: b'%', JL: b'%', 
        JV: b'%', JT: b'%', CB: b'%'}, 
   H2: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'%', JT: b'%', CB: b'_'}, 
   H3: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'%', CB: b'_'}, 
   JL: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'%', H3: b'%', JL: b'%', 
        JV: b'%', JT: b'_', CB: b'_'}, 
   JV: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'%', JT: b'%', CB: b'_'}, 
   JT: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'%', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'%', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'%', HY: b'%', BA: b'%', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'%', CB: b'_'}, 
   CB: {OP: b'_', CL: b'^', CP: b'^', QU: b'%', GL: b'%', NS: b'_', EX: b'^', 
        SY: b'^', IS: b'^', PR: b'_', PO: b'_', NU: b'_', AL: b'_', 
        ID: b'_', IN: b'_', HY: b'_', BA: b'_', BB: b'_', B2: b'_', 
        ZW: b'^', CM: b'#', WJ: b'^', H2: b'_', H3: b'_', JL: b'_', 
        JV: b'_', JT: b'_', CB: b'_'}}

def line_break(c, index=0):
    r"""Return the Line_Break property of `c`
    
    `c` must be a single Unicode code point string.
    
    >>> print(line_break('\x0d'))
    CR
    >>> print(line_break(' '))
    SP
    >>> print(line_break('1'))
    NU
    
    If `index` is specified, this function consider `c` as a unicode 
    string and return Line_Break property of the code point at 
    c[index].
    
    >>> print(line_break(u'a\x0d', 1))
    CR
    """
    return _line_break(code_point(c, index))


def _preprocess_boundaries(s):
    r"""(internal) Preprocess LB9: X CM* -> X
    
    Where X is not in (BK, CR, LF, NL, SP, ZW)
    
    >>> list(_preprocess_boundaries(u'\r\n')) == [(0, 'CR'), (1, 'LF')]
    True
    >>> list(_preprocess_boundaries(u'A\x01A')) == [(0, 'AL'), (2, 'AL')]
    True
    >>> list(_preprocess_boundaries(u'\n\x01')) == [(0, 'LF'), (1, 'CM')]
    True
    >>> list(_preprocess_boundaries(u'\n  A')) == [(0, 'LF'), (1, 'SP'), (2, 'SP'), (3, 'AL')]
    True
    """
    prev_prop = None
    i = 0
    for c in code_points(s):
        prop = line_break(c)
        if prop in (BK, CR, LF, SP, NL, ZW):
            yield (
             i, prop)
            prev_prop = None
        elif prop == CM:
            if prev_prop is None:
                yield (
                 i, prop)
                prev_prop = prop
        else:
            yield (
             i, prop)
            prev_prop = prop
        i += len(c)

    return


def line_break_breakables(s, legacy=False):
    """Iterate line breaking opportunities for every position of `s`
    
    1 means "break" and 0 means "do not break" BEFORE the postion.  
    The length of iteration will be the same as ``len(s)``.
    
    >>> list(line_break_breakables('ABC'))
    [0, 0, 0]
    >>> list(line_break_breakables('Hello, world.'))
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    >>> list(line_break_breakables(u''))
    []
    """
    if not s:
        return
    primitive_boundaries = list(_preprocess_boundaries(s))
    prev_prev_lb = None
    prev_lb = None
    for i, (pos, lb) in enumerate(primitive_boundaries):
        next_pos, __ = primitive_boundaries[(i + 1)] if i < len(primitive_boundaries) - 1 else (len(s), None)
        if legacy:
            if lb == AL:
                cp = unichr(ord(s, pos))
                lb = ID if east_asian_width(cp) == b'A' else AL
            elif lb == AI:
                lb = ID
        else:
            if lb == AI:
                lb = AL
            if lb == CJ:
                lb = NS
            if lb in (CM, XX, SA):
                lb = AL
            if pos == 0:
                do_break = False
            elif prev_lb == BK:
                do_break = True
            elif prev_lb in (CR, LF, NL):
                do_break = not (prev_lb == CR and lb == LF)
            elif lb in (BK, CR, LF, NL):
                do_break = False
            elif lb in (SP, ZW):
                do_break = False
            elif prev_prev_lb == ZW and prev_lb == SP or prev_lb == ZW:
                do_break = True
            elif lb == WJ or prev_lb == WJ:
                do_break = False
            elif prev_lb == GL:
                do_break = False
            elif prev_lb not in (SP, BA, HY) and lb == GL:
                do_break = False
            elif lb in (CL, CP, EX, IS, SY):
                do_break = False
            elif prev_prev_lb == OP and prev_lb == SP or prev_lb == OP:
                do_break = False
            elif prev_prev_lb == QU and prev_lb == SP and lb == OP or prev_lb == QU and lb == OP:
                do_break = False
            elif prev_prev_lb in (CL, CP) and prev_lb == SP and lb == NS or prev_lb in (CL, CP) and lb == NS:
                do_break = False
            elif prev_prev_lb == B2 and prev_lb == SP and lb == B2 or prev_lb == B2 and lb == B2:
                do_break = False
            elif prev_lb == SP:
                do_break = True
            elif lb == QU or prev_lb == QU:
                do_break = False
            elif lb == CB or prev_lb == CB:
                do_break = True
            elif lb in (BA, HY, NS) or prev_lb == BB:
                do_break = False
            elif prev_lb in (AL, HL, ID, IN, NU) and lb == IN:
                do_break = False
            elif prev_lb == ID and lb == PO or prev_lb in (AL, HL) and lb == NU or prev_lb == NU and lb in (AL, HL):
                do_break = False
            elif prev_lb == PR and lb == ID or prev_lb == PR and lb in (AL, HL) or prev_lb == PO and lb in (AL, HL):
                do_break = False
            elif prev_lb == CL and lb == PO or prev_lb == CP and lb == PO or prev_lb == CL and lb == PR or prev_lb == CP and lb == PR or prev_lb == NU and lb == PO or prev_lb == NU and lb == PR or prev_lb == PO and lb == OP or prev_lb == PO and lb == NU or prev_lb == PR and lb == OP or prev_lb == PR and lb == NU or prev_lb == HY and lb == NU or prev_lb == IS and lb == NU or prev_lb == NU and lb == NU or prev_lb == SY and lb == NU:
                do_break = False
            elif prev_lb == JL and lb in (JL, JV, H2, H3) or prev_lb in (JV, H2) and lb in (JV, JT) or prev_lb in (JT, H3) and lb == JT:
                do_break = False
            elif prev_lb in (JL, JV, JT, H2, H3) and lb in (IN, PO) or prev_lb == PR and lb in (JL, JV, JT, H2, H3):
                do_break = False
            elif prev_lb in (AL, HL) and lb in (AL, HL):
                do_break = False
            elif prev_lb == IS and lb in (AL, HL):
                do_break = False
            elif prev_lb in (AL, HL, NU) and lb == OP or prev_lb == CP and lb in (AL, HL, NU):
                do_break = False
            elif prev_lb == lb == RI:
                do_break = False
            else:
                do_break = True
            for j in range(next_pos - pos):
                yield int(j == 0 and do_break)

        prev_prev_lb = prev_lb
        prev_lb = lb

    return


def line_break_boundaries(s, legacy=False, tailor=None):
    """Iterate indices of the line breaking boundaries of `s`
    
    This function yields from 0 to the end of the string (== len(s)).
    """
    breakables = line_break_breakables(s, legacy)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return boundaries(breakables)


def line_break_units(s, legacy=False, tailor=None):
    u"""Iterate every line breaking token of `s`
    
    >>> s = 'The quick (“brown”) fox can’t jump 32.3 feet, right?'
    >>> '|'.join(line_break_units(s)) == 'The |quick |(“brown”) |fox |can’t |jump |32.3 |feet, |right?'
    True
    >>> list(line_break_units(u''))
    []
    
    >>> list(line_break_units('αα')) == [u'αα']
    True
    >>> list(line_break_units(u'αα', True)) == [u'α', u'α']
    True
    """
    breakables = line_break_breakables(s, legacy)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return break_units(s, breakables)


if __name__ == b'__main__':
    import doctest
    doctest.testmod()