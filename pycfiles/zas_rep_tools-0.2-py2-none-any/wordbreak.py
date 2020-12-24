# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/wordbreak.py
# Compiled at: 2018-07-23 18:20:27
"""Unicode word breaking

UAX #29: Unicode Text Segmentation (Unicode 6.2.0)
http://www.unicode.org/reports/tr29/tr29-21.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from .breaking import boundaries, break_units
from .codepoint import code_point, code_points
from .db import word_break as _word_break
__all__ = [
 b'word_break',
 b'word_breakables',
 b'word_boundaries',
 b'words']
Other = b'Other'
CR = b'CR'
LF = b'LF'
Newline = b'Newline'
Extend = b'Extend'
Regional_Indicator = b'Regional_Indicator'
Format = b'Format'
Katakana = b'Katakana'
ALetter = b'ALetter'
MidNumLet = b'MidNumLet'
MidLetter = b'MidLetter'
MidNum = b'MidNum'
Numeric = b'Numeric'
ExtendNumLet = b'ExtendNumLet'
ALetter_FormatFE = b'ALetter_FormatFE'
ALetter_MidLetter = b'ALetter_MidLetter'
ALetter_MidNumLet = b'ALetter_MidNumLet'
ALetter_MidNumLet_FormatFE = b'ALetter_MidNumLet_FormatFE'
ALetter_MidNum = b'ALetter_MidNum'
Numeric_MidLetter = b'Numeric_MidLetter'
Numeric_MidNumLet = b'Numeric_MidNumLet'
Numeric_MidNum = b'Numeric_MidNum'
Numeric_MidNumLet_FormatFE = b'Numeric_MidNumLet_FormatFE'
break_table_index = [
 Other,
 CR,
 LF,
 Newline,
 Katakana,
 ALetter,
 MidLetter,
 MidNum,
 MidNumLet,
 Numeric,
 ExtendNumLet,
 Regional_Indicator,
 Format,
 Extend,
 ALetter_FormatFE,
 ALetter_MidLetter,
 ALetter_MidNumLet,
 ALetter_MidNumLet_FormatFE,
 ALetter_MidNum,
 Numeric_MidLetter,
 Numeric_MidNumLet,
 Numeric_MidNum,
 Numeric_MidNumLet_FormatFE]
break_table = [
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [
  1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
 [
  1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
 [
  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0]]

def word_break(c, index=0):
    ur"""Return the Word_Break property of `c`
    
    `c` must be a single Unicode code point string.
    
    >>> print(word_break('\x0d'))
    CR
    >>> print(word_break('\x0b'))
    Newline
    >>> print(word_break('ア'))
    Katakana
    
    If `index` is specified, this function consider `c` as a unicode 
    string and return Word_Break property of the code point at 
    c[index].
    
    >>> print(word_break('Aア', 1))
    Katakana
    """
    return _word_break(code_point(c, index))


def _preprocess_boundaries(s):
    u"""(internal) Preprocess WB4; X [Extend Format]* -> X
    
    >>> result = list(_preprocess_boundaries('\\r\\n'))
    >>> result == [(0, 'CR'), (1, 'LF')]
    True
    >>> result = list(_preprocess_boundaries('ÄA'))
    >>> result == [(0, 'ALetter'), (2, 'ALetter')]
    True
    >>> result = list(_preprocess_boundaries('\\n\u2060'))
    >>> result == [(0, 'LF'), (1, 'Format')]
    True
    >>> result = list(_preprocess_boundaries('\\x01̈\\x01'))
    >>> result == [(0, 'Other'), (2, 'Other')]
    True
    """
    prev_prop = None
    i = 0
    for c in code_points(s):
        prop = word_break(c)
        if prop in (Newline, CR, LF):
            yield (
             i, prop)
            prev_prop = None
        elif prop in (Extend, Format):
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


def word_breakables(s):
    ur"""Iterate word breaking opportunities for every position of `s`
    
    1 for "break" and 0 for "do not break".  The length of iteration 
    will be the same as ``len(s)``.
    
    >>> list(word_breakables(u'ABC'))
    [1, 0, 0]
    >>> list(word_breakables(u'Hello, world.'))
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1]
    >>> list(word_breakables(u'\x01̈\x01'))
    [1, 0, 1]
    """
    if not s:
        return
    else:
        primitive_boundaries = list(_preprocess_boundaries(s))
        prev_prev_wb = None
        prev_wb = None
        prev_pos = 0
        for i, (pos, wb) in enumerate(primitive_boundaries):
            next_pos, next_wb = primitive_boundaries[(i + 1)] if i < len(primitive_boundaries) - 1 else (len(s), None)
            if prev_wb in (Newline, CR, LF) or wb in (Newline, CR, LF):
                do_break = not (prev_wb == CR and wb == LF)
            else:
                if prev_wb == wb == ALetter:
                    do_break = False
                elif prev_wb == next_wb == ALetter and wb in (MidLetter, MidNumLet):
                    do_break = False
                elif prev_prev_wb == wb == ALetter and prev_wb in (MidLetter, MidNumLet):
                    do_break = False
                elif prev_wb == wb == Numeric:
                    do_break = False
                elif prev_wb == ALetter and wb == Numeric:
                    do_break = False
                elif prev_wb == Numeric and wb == ALetter:
                    do_break = False
                elif prev_prev_wb == wb == Numeric and prev_wb in (MidNum, MidNumLet):
                    do_break = False
                elif prev_wb == next_wb == Numeric and wb in (MidNum, MidNumLet):
                    do_break = False
                elif prev_wb == wb == Katakana or prev_wb in (ALetter, Numeric, Katakana, ExtendNumLet) and wb == ExtendNumLet or prev_wb == ExtendNumLet and wb in (ALetter, Numeric, Katakana):
                    do_break = False
                elif prev_wb == wb == Regional_Indicator:
                    do_break = False
                else:
                    do_break = True
                for j in range(next_pos - pos):
                    yield int(j == 0 and do_break)

            prev_pos = pos
            prev_prev_wb = prev_wb
            prev_wb = wb

        return


def word_boundaries(s, tailor=None):
    """Iterate indices of the word boundaries of `s`
    
    This function yields indices from the first boundary position (> 0) 
    to the end of the string (== len(s)).
    """
    breakables = word_breakables(s)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return boundaries(breakables)


def words(s, tailor=None):
    u"""Iterate *user-perceived* words of `s`
    
    These examples bellow is from
    http://www.unicode.org/reports/tr29/tr29-15.html#Word_Boundaries
    
    >>> s = 'The quick (“brown”) fox can’t jump 32.3 feet, right?'
    >>> print('|'.join(words(s)))
    The| |quick| |(|“|brown|”|)| |fox| |can’t| |jump| |32.3| |feet|,| |right|?
    >>> list(words(u''))
    []
    """
    breakables = word_breakables(s)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return break_units(s, breakables)


if __name__ == b'__main__':
    import doctest
    doctest.testmod()