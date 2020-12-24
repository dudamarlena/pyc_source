# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/villi/github/Tokenizer/src/tokenizer/tokenizer.py
# Compiled at: 2019-10-24 12:31:11
"""

    Tokenizer for Icelandic text

    Copyright (C) 2019 Miðeind ehf.
    Original author: Vilhjálmur Þorsteinsson

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    The function tokenize() consumes a text string and
    returns a generator of tokens. Each token is a tuple,
    typically having the form (type, word, meaning),
    where type is one of the constants specified in the
    TOK class, word is the original word found in the
    source text, and meaning contains auxiliary information
    depending on the token type (such as the definition of
    an abbreviation, or the day, month and year for dates).

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import namedtuple
import re, datetime, unicodedata
from .abbrev import Abbreviations
from .definitions import *
Tok = namedtuple(b'Tok', [b'kind', b'txt', b'val'])

class TOK():
    """ Token types """
    PUNCTUATION = 1
    TIME = 2
    DATE = 3
    YEAR = 4
    NUMBER = 5
    WORD = 6
    TELNO = 7
    PERCENT = 8
    URL = 9
    ORDINAL = 10
    TIMESTAMP = 11
    CURRENCY = 12
    AMOUNT = 13
    PERSON = 14
    EMAIL = 15
    ENTITY = 16
    UNKNOWN = 17
    DATEABS = 18
    DATEREL = 19
    TIMESTAMPABS = 20
    TIMESTAMPREL = 21
    MEASUREMENT = 22
    NUMWLETTER = 23
    DOMAIN = 24
    HASHTAG = 25
    EMPTY_LINE = 10000
    P_BEGIN = 10001
    P_END = 10002
    S_BEGIN = 11001
    S_END = 11002
    X_END = 12001
    END = frozenset((P_END, S_END, X_END))
    TEXT = frozenset((WORD, PERSON, ENTITY))
    TEXT_EXCL_PERSON = frozenset((WORD, ENTITY))
    descr = {PUNCTUATION: b'PUNCTUATION', 
       TIME: b'TIME', 
       TIMESTAMP: b'TIMESTAMP', 
       TIMESTAMPABS: b'TIMESTAMPABS', 
       TIMESTAMPREL: b'TIMESTAMPREL', 
       DATE: b'DATE', 
       DATEABS: b'DATEABS', 
       DATEREL: b'DATEREL', 
       YEAR: b'YEAR', 
       NUMBER: b'NUMBER', 
       NUMWLETTER: b'NUMBER WITH LETTER', 
       CURRENCY: b'CURRENCY', 
       AMOUNT: b'AMOUNT', 
       MEASUREMENT: b'MEASUREMENT', 
       PERSON: b'PERSON', 
       WORD: b'WORD', 
       UNKNOWN: b'UNKNOWN', 
       TELNO: b'TELNO', 
       PERCENT: b'PERCENT', 
       URL: b'URL', 
       DOMAIN: b'DOMAIN', 
       HASHTAG: b'HASHTAG', 
       EMAIL: b'EMAIL', 
       ORDINAL: b'ORDINAL', 
       ENTITY: b'ENTITY', 
       EMPTY_LINE: b'EMPTY LINE', 
       P_BEGIN: b'BEGIN PARA', 
       P_END: b'END PARA', 
       S_BEGIN: b'BEGIN SENT', 
       S_END: b'END SENT'}

    @staticmethod
    def Punctuation(w):
        tp = TP_CENTER
        if w:
            if w[0] in LEFT_PUNCTUATION:
                tp = TP_LEFT
            elif w[0] in RIGHT_PUNCTUATION:
                tp = TP_RIGHT
            elif w[0] in NONE_PUNCTUATION:
                tp = TP_NONE
        return Tok(TOK.PUNCTUATION, w, tp)

    @staticmethod
    def Time(w, h, m, s):
        return Tok(TOK.TIME, w, (h, m, s))

    @staticmethod
    def Date(w, y, m, d):
        return Tok(TOK.DATE, w, (y, m, d))

    @staticmethod
    def Dateabs(w, y, m, d):
        return Tok(TOK.DATEABS, w, (y, m, d))

    @staticmethod
    def Daterel(w, y, m, d):
        return Tok(TOK.DATEREL, w, (y, m, d))

    @staticmethod
    def Timestamp(w, y, mo, d, h, m, s):
        return Tok(TOK.TIMESTAMP, w, (y, mo, d, h, m, s))

    @staticmethod
    def Timestampabs(w, y, mo, d, h, m, s):
        return Tok(TOK.TIMESTAMPABS, w, (y, mo, d, h, m, s))

    @staticmethod
    def Timestamprel(w, y, mo, d, h, m, s):
        return Tok(TOK.TIMESTAMPREL, w, (y, mo, d, h, m, s))

    @staticmethod
    def Year(w, n):
        return Tok(TOK.YEAR, w, n)

    @staticmethod
    def Telno(w, telno):
        return Tok(TOK.TELNO, w, telno)

    @staticmethod
    def Email(w):
        return Tok(TOK.EMAIL, w, None)

    @staticmethod
    def Number(w, n, cases=None, genders=None):
        return Tok(TOK.NUMBER, w, (n, cases, genders))

    @staticmethod
    def NumberWithLetter(w, n, l):
        return Tok(TOK.NUMWLETTER, w, (n, l))

    @staticmethod
    def Currency(w, iso, cases=None, genders=None):
        return Tok(TOK.CURRENCY, w, (iso, cases, genders))

    @staticmethod
    def Amount(w, iso, n, cases=None, genders=None):
        return Tok(TOK.AMOUNT, w, (n, iso, cases, genders))

    @staticmethod
    def Percent(w, n, cases=None, genders=None):
        return Tok(TOK.PERCENT, w, (n, cases, genders))

    @staticmethod
    def Ordinal(w, n):
        return Tok(TOK.ORDINAL, w, n)

    @staticmethod
    def Url(w):
        return Tok(TOK.URL, w, None)

    @staticmethod
    def Domain(w):
        return Tok(TOK.DOMAIN, w, None)

    @staticmethod
    def Hashtag(w):
        return Tok(TOK.HASHTAG, w, None)

    @staticmethod
    def Measurement(w, unit, val):
        return Tok(TOK.MEASUREMENT, w, (unit, val))

    @staticmethod
    def Word(w, m=None):
        return Tok(TOK.WORD, w, m)

    @staticmethod
    def Unknown(w):
        return Tok(TOK.UNKNOWN, w, None)

    @staticmethod
    def Person(w, m=None):
        return Tok(TOK.PERSON, w, m)

    @staticmethod
    def Entity(w):
        return Tok(TOK.ENTITY, w, None)

    @staticmethod
    def Begin_Paragraph():
        return Tok(TOK.P_BEGIN, None, None)

    @staticmethod
    def End_Paragraph():
        return Tok(TOK.P_END, None, None)

    @staticmethod
    def Begin_Sentence(num_parses=0, err_index=None):
        return Tok(TOK.S_BEGIN, None, (num_parses, err_index))

    @staticmethod
    def End_Sentence():
        return Tok(TOK.S_END, None, None)

    @staticmethod
    def End_Sentinel():
        return Tok(TOK.X_END, None, None)

    @staticmethod
    def Empty_Line():
        return Tok(TOK.EMPTY_LINE, None, None)


def is_valid_date(y, m, d):
    """ Returns True if y, m, d is a valid date """
    if 1776 <= y <= 2100 and 1 <= m <= 12 and 1 <= d <= 31:
        try:
            datetime.datetime(year=y, month=m, day=d)
            return True
        except ValueError:
            pass

    return False


def parse_digits(w, convert_numbers):
    """ Parse a raw token starting with a digit """
    s = re.match(b'^\\d{1,2}:\\d\\d:\\d\\d(?!\\d)', w)
    if s:
        g = s.group()
        p = g.split(b':')
        h = int(p[0])
        m = int(p[1])
        sec = int(p[2])
        if 0 <= h < 24 and 0 <= m < 60 and 0 <= sec < 60:
            return (TOK.Time(g, h, m, sec), s.end())
    s = re.match(b'^\\d{1,2}:\\d\\d(?!\\d)', w)
    if s:
        g = s.group()
        p = g.split(b':')
        h = int(p[0])
        m = int(p[1])
        if 0 <= h < 24 and 0 <= m < 60:
            return (TOK.Time(g, h, m, 0), s.end())
    s = re.match(b'^\\d{4}-\\d\\d-\\d\\d(?!\\d)', w) or re.match(b'^\\d{4}/\\d\\d/\\d\\d(?!\\d)', w)
    if s:
        g = s.group()
        if b'-' in g:
            p = g.split(b'-')
        else:
            p = g.split(b'/')
        y = int(p[0])
        m = int(p[1])
        d = int(p[2])
        if is_valid_date(y, m, d):
            return (TOK.Date(g, y, m, d), s.end())
    s = re.match(b'^\\d{1,2}\\.\\d{1,2}\\.\\d{2,4}(?!\\d)', w) or re.match(b'^\\d{1,2}/\\d{1,2}/\\d{2,4}(?!\\d)', w)
    if s:
        g = s.group()
        if b'/' in g:
            p = g.split(b'/')
        else:
            p = g.split(b'.')
        y = int(p[2])
        if y <= 99:
            y += 2000
        m = int(p[1])
        d = int(p[0])
        if m > 12 >= d:
            m, d = d, m
        if is_valid_date(y, m, d):
            return (TOK.Date(g, y, m, d), s.end())
    s = re.match(b'^\\d+([a-zA-Z])(?!\\w)', w, re.UNICODE)
    if s:
        g = s.group()
        l = g[-1:]
        if l not in SI_UNITS.keys():
            n = int(g[:-1])
            return (
             TOK.NumberWithLetter(g, n, l), s.end())
    s = re.match(b'^(\\d+)([¼-¾⅐-⅞])', w)
    if s:
        g = s.group()
        ln = s.group(1)
        vf = s.group(2)
        val = float(ln) + unicodedata.numeric(vf)
        return (
         TOK.Number(g, val), s.end())
    s = re.match(b'^\\d+(\\.\\d\\d\\d)*,\\d+(?!\\d*\\.\\d)', w)
    if s:
        g = s.group()
        n = re.sub(b'\\.', b'', g)
        n = re.sub(b',', b'.', n)
        return (
         TOK.Number(g, float(n)), s.end())
    s = re.match(b'^\\d+(\\.\\d\\d\\d)+(?!\\d)', w)
    if s:
        g = s.group()
        n = re.sub(b'\\.', b'', g)
        return (
         TOK.Number(g, int(n)), s.end())
    s = re.match(b'^\\d{1,2}/\\d{1,2}(?!\\d)', w)
    if s:
        g = s.group()
        p = g.split(b'/')
        m = int(p[1])
        d = int(p[0])
        if p[0][0] != b'0' and p[1][0] != b'0' and (d <= 5 and m <= 6 or d == 1 and m <= 10):
            return (
             TOK.Number(g, float(d) / m), s.end())
        if m > 12 >= d:
            m, d = d, m
        if 1 <= d <= 31 and 1 <= m <= 12:
            return (
             TOK.Date(g, 0, m, d), s.end())
    s = re.match(b'^\\d\\d\\d\\d(?!\\d)', w)
    if s:
        n = int(s.group())
        if 1776 <= n <= 2100:
            return (
             TOK.Year(w[0:4], n), 4)
    s = re.match(b'^\\d\\d\\d\\-\\d\\d\\d\\d(?!\\d)', w)
    if s and w[0] in TELNO_PREFIXES:
        telno = s.group()
        return (
         TOK.Telno(telno, telno), 8)
    s = re.match(b'^\\d\\d\\d\\d\\d\\d\\d(?!\\d)', w)
    if s and w[0] in TELNO_PREFIXES:
        telno = w[0:3] + b'-' + w[3:7]
        return (
         TOK.Telno(w[0:7], telno), 7)
    s = re.match(b'^\\d+\\.\\d+(\\.\\d+)+', w)
    if s:
        g = s.group()
        n = re.sub(b'\\.', b'', g)
        return (
         TOK.Ordinal(g, int(n)), s.end())
    s = re.match(b'^\\d+(,\\d\\d\\d)*\\.\\d+', w)
    if s:
        g = s.group()
        n = re.sub(b',', b'', g)
        if convert_numbers:
            g = re.sub(b',', b'x', g)
            g = re.sub(b'\\.', b',', g)
            g = re.sub(b'x', b'.', g)
        return (TOK.Number(g, float(n)), s.end())
    s = re.match(b'^\\d+(,\\d\\d\\d)*', w)
    if s:
        g = s.group()
        n = re.sub(b',', b'', g)
        if convert_numbers:
            g = re.sub(b',', b'.', g)
        return (TOK.Number(g, int(n)), s.end())
    return (
     TOK.Unknown(w), len(w))


def gen_from_string(txt, replace_composite_glyphs=True):
    """ Generate rough tokens from a string """
    if replace_composite_glyphs:
        txt = UNICODE_REGEX.sub(lambda match: UNICODE_REPLACEMENTS[match.group(0)], txt)
    for w in txt.split():
        yield w


def gen(txt_or_gen, replace_composite_glyphs=True):
    """ Generate rough tokens from a string or a generator """
    if txt_or_gen is None:
        return
    else:
        if is_str(txt_or_gen):
            txt_or_gen = [
             txt_or_gen]
        for txt in txt_or_gen:
            txt = txt.strip()
            if not txt:
                yield b''
            else:
                txt = make_str(txt)
                for w in gen_from_string(txt, replace_composite_glyphs):
                    yield w

        return


def parse_tokens(txt, options):
    """ Generator that parses contiguous text into a stream of tokens """
    convert_numbers = options.get(b'convert_numbers', False)
    replace_composite_glyphs = options.get(b'replace_composite_glyphs', True)
    handle_kludgy_ordinals = options.get(b'handle_kludgy_ordinals', KLUDGY_ORDINALS_PASS_THROUGH)
    for w in gen(txt, replace_composite_glyphs):
        qmark = False
        if not w:
            yield TOK.Empty_Line()
            continue
        if w.isalpha() or w in SI_UNITS:
            yield TOK.Word(w, None)
            continue
        if len(w) > 2:
            if w[0] in DQUOTES and w[(-1)] in DQUOTES:
                yield TOK.Punctuation(b'„')
                if w[1:-1].isalpha():
                    yield TOK.Word(w[1:-1], None)
                    yield TOK.Punctuation(b'“')
                    continue
                w = w[1:-1] + b'“'
                qmark = True
            elif w[0] in SQUOTES and w[(-1)] in SQUOTES:
                yield TOK.Punctuation(b'‚')
                if w[1:-1].isalpha():
                    yield TOK.Word(w[1:-1], None)
                    yield TOK.Punctuation(b'‘')
                    continue
                w = w[1:-1] + b'‘'
                qmark = True
        if len(w) > 1:
            if w[0] in DQUOTES:
                yield TOK.Punctuation(b'„')
                w = w[1:]
            elif w[0] in SQUOTES:
                yield TOK.Punctuation(b'‚')
                w = w[1:]
        while w:
            ate = False
            while w and w[0] in PUNCTUATION:
                ate = True
                lw = len(w)
                if w.startswith(b'[...]'):
                    yield TOK.Punctuation(b'[…]')
                    w = w[5:]
                elif w.startswith(b'[…]'):
                    yield TOK.Punctuation(b'[…]')
                    w = w[3:]
                elif w.startswith(b'...'):
                    yield TOK.Punctuation(b'…')
                    w = w[3:]
                elif w == b',,':
                    yield TOK.Punctuation(b',')
                    w = b''
                elif w.startswith(b',,'):
                    yield TOK.Punctuation(b'„')
                    w = w[2:]
                elif lw == 2 and (w == b'[[' or w == b']]'):
                    if w == b'[[':
                        yield TOK.Begin_Paragraph()
                    else:
                        yield TOK.End_Paragraph()
                    w = w[2:]
                elif w[0] in HYPHENS:
                    yield TOK.Punctuation(HYPHEN)
                    w = w[1:]
                    while w and w[0] in HYPHENS:
                        w = w[1:]

                elif lw == 1 and w in DQUOTES:
                    yield TOK.Punctuation(b'“')
                    w = b''
                    qmark = False
                elif lw == 1 and w in SQUOTES:
                    yield TOK.Punctuation(b'‘')
                    w = b''
                    qmark = False
                elif lw > 1 and w.startswith(b'#'):
                    ate = False
                    break
                else:
                    yield TOK.Punctuation(w[0])
                    w = w[1:]

            if w and b'@' in w:
                s = re.match(b'^[^@\\s]+@[^@\\s]+(\\.[^@\\s\\.,/:;\\"\\(\\)%#!\\?”]+)+', w)
                if s:
                    ate = True
                    yield TOK.Email(s.group())
                    w = w[s.end():]
            if w and w[0] in SINGLECHAR_FRACTIONS:
                ate = True
                yield TOK.Number(w[0], unicodedata.numeric(w[0]))
                w = w[1:]
            if w and w.startswith(URL_PREFIXES):
                endp = b''
                while w and w[(-1)] in RIGHT_PUNCTUATION:
                    endp = w[(-1)] + endp
                    w = w[:-1]

                yield TOK.Url(w)
                ate = True
                w = endp
            if w and len(w) >= 2 and re.search(b'^#\\w', w, re.UNICODE):
                tag = w[:1]
                w = w[1:]
                while w and w[0] not in PUNCTUATION:
                    tag += w[0]
                    w = w[1:]

                if re.search(b'^#\\d+$', tag):
                    yield TOK.Ordinal(tag, int(tag[1:]))
                else:
                    yield TOK.Hashtag(tag)
                ate = True
            if w and len(w) >= MIN_DOMAIN_LENGTH and w[0].isalnum() and b'.' in w[1:-2] and DOMAIN_REGEX.search(w):
                endp = b''
                while w and w[(-1)] in PUNCTUATION:
                    endp = w[(-1)] + endp
                    w = w[:-1]

                yield TOK.Domain(w)
                ate = True
                w = endp
            if w and w[0] in DIGITS:
                for key, val in items(ORDINAL_ERRORS):
                    if w.startswith(key):
                        if handle_kludgy_ordinals == KLUDGY_ORDINALS_MODIFY:
                            yield TOK.Word(val)
                        elif handle_kludgy_ordinals == KLUDGY_ORDINALS_TRANSLATE and key in ORDINAL_NUMBERS:
                            yield TOK.Ordinal(key, ORDINAL_NUMBERS[key])
                        else:
                            yield TOK.Word(key)
                        eaten = len(key)
                        break
                else:
                    t, eaten = parse_digits(w, convert_numbers)
                    yield t

                ate = True
                w = w[eaten:]
                if w in SI_UNITS:
                    yield TOK.Word(w, None)
                    w = b''
            if w and w[0].isalpha():
                ate = True
                i = 1
                lw = len(w)
                while i < lw and (w[i].isalpha() or w[i] in PUNCT_INSIDE_WORD and (i + 1 == lw or w[(i + 1)].isalpha())):
                    i += 1

                a = w.split(b'.')
                if len(a) == 2 and a[0] and a[0][0].islower() and a[1] and a[1][0].isupper():
                    yield TOK.Word(a[0])
                    yield TOK.Punctuation(b'.')
                    yield TOK.Word(a[1])
                    w = None
                else:
                    while w[(i - 1)] == b'.':
                        i -= 1

                    yield TOK.Word(w[0:i])
                    w = w[i:]
                    if w and w[0] in COMPOSITE_HYPHENS:
                        yield TOK.Punctuation(COMPOSITE_HYPHEN)
                        w = w[1:]
                    if qmark and w and w[:-1].isalpha():
                        yield TOK.Word(w[:-1])
                        w = w[-1:]
                        if w in SQUOTES:
                            yield TOK.Punctuation(b'‘')
                            w = b''
                        elif w in DQUOTES:
                            yield TOK.Punctuation(b'“')
                            w = b''
                        qmark = False
            if not ate:
                yield TOK.Unknown(w[0])
                w = w[1:]
            if w:
                if w[0] in DQUOTES:
                    w = b'“' + w[1:]
                elif w[0] in SQUOTES:
                    w = b'‘' + w[1:]

    yield TOK.End_Sentinel()
    return


def parse_particles(token_stream, options):
    """ Parse a stream of tokens looking for 'particles'
        (simple token pairs and abbreviations) and making substitutions """

    def is_abbr_with_period(txt):
        """ Return True if the given token text is an abbreviation
            when followed by a period """
        if b'.' in txt and txt not in Abbreviations.DICT:
            return True
        if txt in Abbreviations.SINGLES:
            return True
        if txt.lower() in Abbreviations.SINGLES:
            return txt not in Abbreviations.DICT
        return False

    def lookup(abbrev):
        """ Look up an abbreviation, both in original case and in lower case,
            and return either None if not found or a meaning list having one entry """
        m = Abbreviations.DICT.get(abbrev)
        if m is not None:
            return [m]
        else:
            m = Abbreviations.DICT.get(abbrev.lower())
            if m is None:
                return
            return [m]

    token = None
    try:
        token = next(token_stream)
        while True:
            next_token = next(token_stream)
            clock = False
            if token.txt in CURRENCY_SYMBOLS:
                for symbol, currabbr in CURRENCY_SYMBOLS.items():
                    if token.kind == TOK.PUNCTUATION and token.txt == symbol and next_token.kind == TOK.NUMBER:
                        token = TOK.Amount(token.txt + next_token.txt, currabbr, next_token.val[0])
                        next_token = next(token_stream)
                        break

            if next_token.kind == TOK.PUNCTUATION and next_token.txt == b'.' and token.kind == TOK.WORD and token.txt[(-1)] != b'.':
                if is_abbr_with_period(token.txt):
                    clock = token.txt.lower() == CLOCK_ABBREV
                    follow_token = next(token_stream)
                    abbrev = token.txt + b'.'
                    if abbrev in Abbreviations.NAME_FINISHERS:
                        test_set = TOK.TEXT_EXCL_PERSON
                    else:
                        test_set = TOK.TEXT
                    finish = follow_token.kind in TOK.END or follow_token.kind in test_set and follow_token.txt[0].isupper() and follow_token.txt.lower() not in MONTHS and not RE_ROMAN_NUMERAL.match(follow_token.txt) and not (abbrev in MULTIPLIERS and follow_token.txt in CURRENCY_ABBREV)
                    if finish:
                        if abbrev in Abbreviations.FINISHERS:
                            token = TOK.Word(token.txt, lookup(abbrev))
                            yield token
                            token = next_token
                        elif abbrev in Abbreviations.NOT_FINISHERS:
                            yield token
                            token = next_token
                        else:
                            token = TOK.Word(abbrev, lookup(abbrev))
                    else:
                        token = TOK.Word(abbrev, lookup(abbrev))
                    next_token = follow_token
            if next_token.kind == TOK.TIME or next_token.kind == TOK.NUMBER:
                if clock or token.kind == TOK.WORD and token.txt.lower() == CLOCK_WORD:
                    txt = CLOCK_ABBREV + b'.' if clock else token.txt
                    if next_token.kind == TOK.NUMBER:
                        a = (b'{0:.2f}').format(next_token.val[0]).split(b'.')
                        h, m = int(a[0]), int(a[1])
                        token = TOK.Time(txt + b' ' + next_token.txt, h, m, 0)
                    else:
                        token = TOK.Time(txt + b' ' + next_token.txt, next_token.val[0], next_token.val[1], next_token.val[2])
                    next_token = next(token_stream)
            elif next_token.txt in CLOCK_NUMBERS:
                if clock or token.kind == TOK.WORD and token.txt.lower() == CLOCK_WORD:
                    txt = CLOCK_ABBREV + b'.' if clock else token.txt
                    token = TOK.Time((txt + b' ' + next_token.txt), *CLOCK_NUMBERS[next_token.txt])
                    next_token = next(token_stream)
            if token.txt in CLOCK_HALF:
                token = TOK.Time(token.txt, *CLOCK_NUMBERS[token.txt])
            if token.kind == TOK.WORD and token.txt.lower() in YEAR_WORD and (next_token.kind == TOK.YEAR or next_token.kind == TOK.NUMBER):
                token = TOK.Year(token.txt + b' ' + next_token.txt, next_token.val if next_token.kind == TOK.YEAR else next_token.val[0])
                next_token = next(token_stream)
            if token.kind == TOK.NUMBER and (next_token.kind == TOK.NUMBER or next_token.kind == TOK.YEAR) and token.txt[0] in TELNO_PREFIXES and re.search(b'^\\d\\d\\d$', token.txt) and re.search(b'^\\d\\d\\d\\d$', next_token.txt):
                w = token.txt + b' ' + next_token.txt
                telno = token.txt + b'-' + next_token.txt
                token = TOK.Telno(w, telno)
                next_token = next(token_stream)
            if next_token.kind == TOK.PUNCTUATION and next_token.txt == b'%':
                if token.kind == TOK.NUMBER:
                    token = TOK.Percent(token.txt + b'%', token.val[0])
                    next_token = next(token_stream)
            if next_token.kind == TOK.PUNCTUATION and next_token.txt == b'.':
                if token.kind == TOK.NUMBER and not (b'.' in token.txt or b',' in token.txt) or token.kind == TOK.WORD and RE_ROMAN_NUMERAL.match(token.txt) and token.txt not in Abbreviations.DICT:
                    follow_token = next(token_stream)
                    if follow_token.kind in TOK.END or follow_token.kind == TOK.PUNCTUATION and follow_token.txt in {b'„', b'"'} or follow_token.kind == TOK.WORD and follow_token.txt[0].isupper() and month_for_token(follow_token, True) is None:
                        yield token
                        token = next_token
                        next_token = follow_token
                    else:
                        num = token.val[0] if token.kind == TOK.NUMBER else roman_to_int(token.txt)
                        token = TOK.Ordinal(token.txt + b'.', num)
                        next_token = follow_token
            if (token.kind == TOK.NUMBER or token.kind == TOK.YEAR) and next_token.txt in SI_UNITS:
                value = token.val[0] if token.kind == TOK.NUMBER else token.val
                unit, factor = SI_UNITS[next_token.txt]
                if callable(factor):
                    value = factor(value)
                else:
                    value *= factor
                if next_token.txt in RIGHT_PUNCTUATION:
                    token = TOK.Measurement(token.txt + next_token.txt, unit, value)
                else:
                    token = TOK.Measurement(token.txt + b' ' + next_token.txt, unit, value)
                next_token = next(token_stream)
            if token.kind == TOK.MEASUREMENT and token.val[0] == b'°' and next_token.kind == TOK.WORD and next_token.txt in {b'C', b'F'}:
                new_unit = b'°' + next_token.txt
                unit, factor = SI_UNITS[new_unit]
                if not callable(factor):
                    raise AssertionError
                    token = TOK.Measurement(token.txt[:-1] + b' ' + new_unit, unit, factor(token.val[1]))
                    next_token = next(token_stream)
                if token.kind == TOK.WORD and token.val is None and token.txt in Abbreviations.DICT:
                    token = TOK.Word(token.txt, [Abbreviations.DICT[token.txt]])
            yield token
            token = next_token

    except StopIteration:
        if token:
            yield token

    return


def parse_sentences(token_stream):
    """ Parse a stream of tokens looking for sentences, i.e. substreams within
        blocks delimited by sentence finishers (periods, question marks,
        exclamation marks, etc.) """
    in_sentence = False
    token = None
    tok_begin_sentence = TOK.Begin_Sentence()
    tok_end_sentence = TOK.End_Sentence()
    try:
        token = next(token_stream)
        while True:
            next_token = next(token_stream)
            if token.kind == TOK.P_BEGIN or token.kind == TOK.P_END:
                if in_sentence:
                    yield tok_end_sentence
                    in_sentence = False
                if token.kind == TOK.P_BEGIN and next_token.kind == TOK.P_END:
                    token = None
                    token = next(token_stream)
                    continue
            elif token.kind == TOK.X_END:
                assert not in_sentence
            elif token.kind == TOK.EMPTY_LINE:
                if in_sentence:
                    yield tok_end_sentence
                in_sentence = False
                token = next_token
                continue
            else:
                if not in_sentence:
                    yield tok_begin_sentence
                    in_sentence = True
                if token.kind == TOK.PUNCTUATION and token.txt in END_OF_SENTENCE:
                    while next_token.kind == TOK.PUNCTUATION and next_token.txt in SENTENCE_FINISHERS:
                        yield token
                        token = next_token
                        next_token = next(token_stream)

                    yield token
                    token = tok_end_sentence
                    in_sentence = False
            yield token
            token = next_token

    except StopIteration:
        pass

    if token is not None and token.kind != TOK.EMPTY_LINE:
        if not in_sentence and token.kind not in TOK.END:
            yield tok_begin_sentence
            in_sentence = True
        yield token
        if in_sentence and token.kind in {TOK.S_END, TOK.P_END}:
            in_sentence = False
    if in_sentence:
        yield tok_end_sentence
    return


def match_stem_list(token, stems):
    """ Find the stem of a word token in given dict, or return None if not found """
    if token.kind != TOK.WORD:
        return
    else:
        return stems.get(token.txt.lower(), None)


def month_for_token(token, after_ordinal=False):
    """ Return a number, 1..12, corresponding to a month name,
        or None if the token does not contain a month name """
    if not after_ordinal and token.txt in MONTH_BLACKLIST:
        return None
    else:
        return match_stem_list(token, MONTHS)


def parse_phrases_1(token_stream):
    """ Handle dates and times """
    token = None
    try:
        token = next(token_stream)
        while True:
            next_token = next(token_stream)
            if token.kind == TOK.YEAR or token.kind == TOK.NUMBER:
                val = token.val if token.kind == TOK.YEAR else token.val[0]
                if next_token.txt in BCE:
                    token = TOK.Year(token.txt + b' ' + next_token.txt, -val)
                    next_token = next(token_stream)
                elif next_token.txt in CE:
                    token = TOK.Year(token.txt + b' ' + next_token.txt, val)
                    next_token = next(token_stream)
            if (token.kind == TOK.ORDINAL or token.kind == TOK.NUMBER) and next_token.kind == TOK.WORD:
                month = month_for_token(next_token, True)
                if month is not None:
                    token = TOK.Date(token.txt + b' ' + next_token.txt, y=0, m=month, d=token.val if token.kind == TOK.ORDINAL else token.val[0])
                    next_token = next(token_stream)
            if token.kind == TOK.DATE and next_token.kind == TOK.YEAR:
                if not token.val[0]:
                    token = TOK.Date(token.txt + b' ' + next_token.txt, y=next_token.val, m=token.val[1], d=token.val[2])
                    next_token = next(token_stream)
            if token.kind == TOK.DATE and next_token.kind == TOK.TIME:
                y, mo, d = token.val
                h, m, s = next_token.val
                token = TOK.Timestamp(token.txt + b' ' + next_token.txt, y=y, mo=mo, d=d, h=h, m=m, s=s)
                next_token = next(token_stream)
            yield token
            token = next_token

    except StopIteration:
        pass

    if token:
        yield token
    return


def parse_date_and_time(token_stream):
    """ Handle dates and times, absolute and relative. """
    token = None
    try:
        token = next(token_stream)
        while True:
            next_token = next(token_stream)
            if (token.kind == TOK.ORDINAL or token.kind == TOK.NUMBER or token.txt and token.txt.lower() in DAYS_OF_MONTH) and next_token.kind == TOK.WORD:
                month = month_for_token(next_token, True)
                if month is not None:
                    token = TOK.Date(token.txt + b' ' + next_token.txt, y=0, m=month, d=token.val if token.kind == TOK.ORDINAL else token.val[0] if token.kind == TOK.NUMBER else DAYS_OF_MONTH[token.txt.lower()])
                    next_token = next(token_stream)
            if token.kind == TOK.DATE and (next_token.kind == TOK.NUMBER or next_token.kind == TOK.YEAR):
                if not token.val[0]:
                    year = next_token.val if next_token.kind == TOK.YEAR else next_token.val[0] if 1776 <= next_token.val[0] <= 2100 else 0
                    if year != 0:
                        token = TOK.Date(token.txt + b' ' + next_token.txt, y=year, m=token.val[1], d=token.val[2])
                        next_token = next(token_stream)
            if token.kind == TOK.WORD and (next_token.kind == TOK.NUMBER or next_token.kind == TOK.YEAR):
                month = month_for_token(token)
                if month is not None:
                    year = next_token.val if next_token.kind == TOK.YEAR else next_token.val[0] if 1776 <= next_token.val[0] <= 2100 else 0
                    if year != 0:
                        token = TOK.Date(token.txt + b' ' + next_token.txt, y=year, m=month, d=0)
                        next_token = next(token_stream)
            if token.kind == TOK.WORD:
                month = month_for_token(token)
                if month is not None and token.txt not in {
                 b'jan',
                 b'Jan',
                 b'mar',
                 b'Mar',
                 b'júl',
                 b'Júl',
                 b'des',
                 b'Des',
                 b'Ágúst'}:
                    token = TOK.Daterel(token.txt, y=0, m=month, d=0)
            if token.kind == TOK.DATE:
                if token.val[0] and token.val[1] and token.val[2]:
                    token = TOK.Dateabs(token.txt, y=token.val[0], m=token.val[1], d=token.val[2])
                else:
                    token = TOK.Daterel(token.txt, y=token.val[0], m=token.val[1], d=token.val[2])
            if token.kind == TOK.TIMESTAMP:
                if all(x != 0 for x in token.val[0:3]):
                    token = TOK.Timestampabs(token.txt, *token.val)
                else:
                    token = TOK.Timestamprel(token.txt, *token.val)
            if token.kind == TOK.DATEABS:
                if next_token.kind == TOK.WORD and next_token.txt in CE_BCE:
                    y = token.val[0]
                    if next_token.txt in BCE:
                        y = -y
                    token = TOK.Dateabs(token.txt + b' ' + next_token.txt, y=y, m=token.val[1], d=token.val[2])
                    next_token = next(token_stream)
            if token.kind == TOK.DATEABS:
                if next_token.kind == TOK.TIME:
                    y, mo, d = token.val
                    h, m, s = next_token.val
                    token = TOK.Timestampabs(token.txt + b' ' + next_token.txt, y=y, mo=mo, d=d, h=h, m=m, s=s)
                    next_token = next(token_stream)
            if token.kind == TOK.DATEREL:
                if next_token.kind == TOK.TIME:
                    y, mo, d = token.val
                    h, m, s = next_token.val
                    token = TOK.Timestamprel(token.txt + b' ' + next_token.txt, y=y, mo=mo, d=d, h=h, m=m, s=s)
                    next_token = next(token_stream)
            yield token
            token = next_token

    except StopIteration:
        pass

    if token:
        yield token
    return


def parse_phrases_2(token_stream):
    """ Handle numbers, amounts and composite words. """
    token = None
    try:
        token = next(token_stream)
        while True:
            next_token = next(token_stream)

            def number(tok):
                """ If the token denotes a number, return that number - or None """
                if tok.txt.lower() == b'áttu':
                    return None
                else:
                    return match_stem_list(tok, MULTIPLIERS)

            multiplier = number(token) if token.kind == TOK.WORD else None
            while (token.kind == TOK.NUMBER or multiplier is not None) and next_token.kind == TOK.WORD:
                multiplier_next = number(next_token)

                def convert_to_num(token):
                    if multiplier is not None:
                        token = TOK.Number(token.txt, multiplier)
                    return token

                if multiplier_next is not None:
                    token = convert_to_num(token)
                    token = TOK.Number(token.txt + b' ' + next_token.txt, token.val[0] * multiplier_next)
                    next_token = next(token_stream)
                elif next_token.txt in AMOUNT_ABBREV:
                    token = convert_to_num(token)
                    token = TOK.Amount(token.txt + b' ' + next_token.txt, b'ISK', token.val[0] * AMOUNT_ABBREV[next_token.txt])
                    next_token = next(token_stream)
                elif next_token.txt in CURRENCY_ABBREV:
                    token = TOK.Amount(token.txt + b' ' + next_token.txt, next_token.txt, token.val[0])
                    next_token = next(token_stream)
                else:
                    percentage = match_stem_list(next_token, PERCENTAGES)
                    if percentage is not None:
                        token = convert_to_num(token)
                        token = TOK.Percent(token.txt + b' ' + next_token.txt, token.val[0])
                        next_token = next(token_stream)
                    else:
                        break
                multiplier = None

            if next_token.kind == TOK.NUMBER and (token.txt in ISK_AMOUNT_PRECEDING or token.txt in CURRENCY_ABBREV):
                curr = b'ISK' if token.txt in ISK_AMOUNT_PRECEDING else token.txt
                token = TOK.Amount(token.txt + b' ' + next_token.txt, curr, next_token.val[0])
                next_token = next(token_stream)
            tq = []
            while token.kind == TOK.WORD and next_token.kind == TOK.PUNCTUATION and next_token.txt == COMPOSITE_HYPHEN:
                tq.append(token)
                tq.append(TOK.Punctuation(HYPHEN))
                comma_token = next(token_stream)
                if comma_token.kind == TOK.PUNCTUATION and comma_token.txt == b',':
                    tq.append(comma_token)
                    comma_token = next(token_stream)
                token = comma_token
                next_token = next(token_stream)

            if tq:
                if token.kind == TOK.WORD and (token.txt == b'og' or token.txt == b'eða'):
                    if next_token.kind != TOK.WORD:
                        for t in tq:
                            yield t

                    else:
                        txt = (b' ').join(t.txt for t in tq + [token, next_token])
                        txt = txt.replace(b' -', b'-').replace(b' ,', b',')
                        token = TOK.Word(txt)
                        next_token = next(token_stream)
                elif token.kind == TOK.WORD and len(tq) == 2 and tq[1].txt == HYPHEN and tq[0].txt.lower() in ADJECTIVE_PREFIXES:
                    token = TOK.Word(tq[0].txt + b'-' + token.txt)
                else:
                    for t in tq:
                        yield t

            yield token
            token = next_token

    except StopIteration:
        pass

    if token:
        yield token
    return


def tokenize(text, **options):
    """ Tokenize text in several phases, returning a generator
        (iterable sequence) of tokens that processes tokens on-demand. """
    Abbreviations.initialize()
    with_annotation = options.pop(b'with_annotation', True)
    token_stream = parse_tokens(text, options)
    token_stream = parse_particles(token_stream, options)
    token_stream = parse_sentences(token_stream)
    token_stream = parse_phrases_1(token_stream)
    token_stream = parse_date_and_time(token_stream)
    if with_annotation:
        token_stream = parse_phrases_2(token_stream)
    return (t for t in token_stream if t.kind != TOK.X_END)


def tokenize_without_annotation(text, **options):
    u""" Tokenize without the last pass which can be done more thoroughly if BÍN
        annotation is available, for instance in ReynirPackage. """
    return tokenize(text, with_annotation=False, **options)


def mark_paragraphs(txt):
    """ Insert paragraph markers into plaintext, by newlines """
    if not txt:
        return b'[[ ]]'
    return b'[[ ' + (b' ]] [[ ').join(txt.split(b'\n')) + b' ]]'


def paragraphs(toklist):
    """ Generator yielding paragraphs from a token list. Each paragraph is a list
        of sentence tuples. Sentence tuples consist of the index of the first token
        of the sentence (the TOK.S_BEGIN token) and a list of the tokens within the
        sentence, not including the starting TOK.S_BEGIN or the terminating TOK.S_END
        tokens. """
    if not toklist:
        return

    def valid_sent(sent):
        """ Return True if the token list in sent is a proper
            sentence that we want to process further """
        if not sent:
            return False
        return any(t[0] != TOK.PUNCTUATION for t in sent)

    sent = []
    sent_begin = 0
    current_p = []
    for ix, t in enumerate(toklist):
        t0 = t[0]
        if t0 == TOK.S_BEGIN:
            sent = []
            sent_begin = ix
        elif t0 == TOK.S_END:
            if valid_sent(sent):
                current_p.append((sent_begin, sent))
            sent = []
        elif t0 == TOK.P_BEGIN or t0 == TOK.P_END:
            if valid_sent(sent):
                current_p.append((sent_begin, sent))
            sent = []
            if current_p:
                yield current_p
                current_p = []
        else:
            sent.append(t)

    if valid_sent(sent):
        current_p.append((sent_begin, sent))
    if current_p:
        yield current_p


RE_SPLIT_STR = b'([\\+\\-\\$€]?\\d{1,3}(?:\\.\\d\\d\\d)+\\,\\d+)|([\\+\\-\\$€]?\\d{1,3}(?:\\,\\d\\d\\d)+\\.\\d+)|([\\+\\-\\$€]?\\d+\\,\\d+(?!\\.\\d))|([\\+\\-\\$€]?\\d+\\.\\d+(?!\\,\\d))|([~\\s' + (b'').join(b'\\' + c for c in PUNCTUATION) + b'])'
RE_SPLIT = re.compile(RE_SPLIT_STR)

def correct_spaces(s):
    """ Utility function to split and re-compose a string
        with correct spacing between tokens """
    r = []
    last = TP_NONE
    for w in RE_SPLIT.split(s):
        if w is None:
            continue
        w = w.strip()
        if not w:
            continue
        if len(w) > 1:
            this = TP_WORD
        elif w in LEFT_PUNCTUATION:
            this = TP_LEFT
        elif w in RIGHT_PUNCTUATION:
            this = TP_RIGHT
        elif w in NONE_PUNCTUATION:
            this = TP_NONE
        elif w in CENTER_PUNCTUATION:
            this = TP_CENTER
        else:
            this = TP_WORD
        if TP_SPACE[(last - 1)][(this - 1)] and r:
            r.append(b' ' + w)
        else:
            r.append(w)
        last = this

    return (b'').join(r)