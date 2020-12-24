# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/villi/github/Tokenizer/src/tokenizer/definitions.py
# Compiled at: 2019-10-24 12:45:17
"""

    Definitions used for tokenization of Icelandic text

    Copyright(C) 2019 Miðeind ehf.
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

"""
from __future__ import absolute_import
from __future__ import unicode_literals
import sys, re
if sys.version_info >= (3, 0):
    items = lambda d: d.items()
    keys = lambda d: d.keys()
    make_str = lambda s: s
    unicode_chr = lambda c: chr(c)
    is_str = lambda s: isinstance(s, str)
else:
    items = lambda d: d.iteritems()
    keys = lambda d: d.iterkeys()

    def make_str(s):
        if isinstance(s, unicode):
            return s
        return s.decode(b'utf-8')


    unicode_chr = lambda c: unichr(c)
    is_str = lambda s: isinstance(s, (unicode, str))
CONVERT_NUMBERS = False
CONVERT_TELNOS = False
ACCENT = unicode_chr(769)
UMLAUT = unicode_chr(776)
SOFT_HYPHEN = unicode_chr(173)
ZEROWIDTH_SPACE = unicode_chr(8203)
ZEROWIDTH_NBSP = unicode_chr(65279)
UNICODE_REPLACEMENTS = {b'a' + ACCENT: b'á', 
   b'a' + UMLAUT: b'ä', 
   b'e' + ACCENT: b'é', 
   b'e' + UMLAUT: b'ë', 
   b'i' + ACCENT: b'í', 
   b'o' + ACCENT: b'ó', 
   b'u' + ACCENT: b'ú', 
   b'u' + UMLAUT: b'ü', 
   b'y' + ACCENT: b'ý', 
   b'o' + UMLAUT: b'ö', 
   b'A' + UMLAUT: b'Ä', 
   b'A' + ACCENT: b'Á', 
   b'E' + ACCENT: b'É', 
   b'E' + UMLAUT: b'Ë', 
   b'I' + ACCENT: b'Í', 
   b'O' + ACCENT: b'Ó', 
   b'U' + ACCENT: b'Ú', 
   b'U' + UMLAUT: b'Ü', 
   b'Y' + ACCENT: b'Ý', 
   b'O' + UMLAUT: b'Ö', 
   SOFT_HYPHEN: b'', 
   ZEROWIDTH_SPACE: b'', 
   ZEROWIDTH_NBSP: b''}
UNICODE_REGEX = re.compile((b'|').join(map(re.escape, keys(UNICODE_REPLACEMENTS))))
HYPHEN = b'-'
EN_DASH = b'–'
EM_DASH = b'—'
HYPHENS = HYPHEN + EN_DASH + EM_DASH
COMPOSITE_HYPHENS = HYPHEN + EN_DASH
COMPOSITE_HYPHEN = EN_DASH
LEFT_PUNCTUATION = b'([„‚«#$€£¥₽<'
RIGHT_PUNCTUATION = b'.,:;)]!%?“»”’‛‘…>°'
CENTER_PUNCTUATION = b'"*&+=@©|'
NONE_PUNCTUATION = b"/±'´~\\" + HYPHEN + EN_DASH + EM_DASH
PUNCTUATION = LEFT_PUNCTUATION + CENTER_PUNCTUATION + RIGHT_PUNCTUATION + NONE_PUNCTUATION
PUNCTUATION_REGEX = (b'[{0}]').format((b'|').join(re.escape(p) for p in PUNCTUATION))
TP_LEFT = 1
TP_CENTER = 2
TP_RIGHT = 3
TP_NONE = 4
TP_WORD = 5
TP_SPACE = (
 (
  False, True, False, False, False),
 (
  True, True, True, True, True),
 (
  True, True, False, False, True),
 (
  False, True, False, False, False),
 (
  True, True, False, False, True))
END_OF_SENTENCE = frozenset([b'.', b'?', b'!', b'…'])
SENTENCE_FINISHERS = frozenset([b')', b']', b'“', b'»', b'”', b'’', b'"', b'[…]'])
PUNCT_INSIDE_WORD = frozenset([b'.', b"'", b'‘', b'´', b'’'])
SQUOTES = b"'‚‛‘´"
DQUOTES = b'"“„”«»'
CLOCK_WORD = b'klukkan'
CLOCK_ABBREV = b'kl'
TELNO_PREFIXES = b'45678'
ADJECTIVE_PREFIXES = frozenset(('hálf', 'marg', 'semí', 'full'))
YEAR_WORD = frozenset(('árið', 'ársins', 'árinu'))
DIGITS = frozenset([ d for d in b'0123456789' ])
MONTHS = {b'janúar': 1, 
   b'janúars': 1, 
   b'febrúar': 2, 
   b'febrúars': 2, 
   b'mars': 3, 
   b'apríl': 4, 
   b'apríls': 4, 
   b'maí': 5, 
   b'maís': 5, 
   b'júní': 6, 
   b'júnís': 6, 
   b'júlí': 7, 
   b'júlís': 7, 
   b'ágúst': 8, 
   b'ágústs': 8, 
   b'september': 9, 
   b'septembers': 9, 
   b'október': 10, 
   b'októbers': 10, 
   b'nóvember': 11, 
   b'nóvembers': 11, 
   b'desember': 12, 
   b'desembers': 12, 
   b'jan.': 1, 
   b'feb.': 2, 
   b'mar.': 3, 
   b'apr.': 4, 
   b'jún.': 6, 
   b'júl.': 7, 
   b'ág.': 8, 
   b'ágú.': 8, 
   b'sep.': 9, 
   b'sept.': 9, 
   b'okt.': 10, 
   b'nóv.': 11, 
   b'des.': 12, 
   b'jan': 1, 
   b'feb': 2, 
   b'mar': 3, 
   b'apr': 4, 
   b'jún': 6, 
   b'júl': 7, 
   b'ág': 8, 
   b'ágú': 8, 
   b'sep': 9, 
   b'sept': 9, 
   b'okt': 10, 
   b'nóv': 11, 
   b'des': 12}
MONTH_BLACKLIST = frozenset(('Ágúst', ))
DAYS_OF_MONTH = {b'fyrsti': 1, 
   b'fyrsta': 1, 
   b'annar': 2, 
   b'annan': 2, 
   b'þriðji': 3, 
   b'þriðja': 3, 
   b'fjórði': 4, 
   b'fjórða': 4, 
   b'fimmti': 5, 
   b'fimmta': 5, 
   b'sjötti': 6, 
   b'sjötta': 6, 
   b'sjöundi': 7, 
   b'sjöunda': 7, 
   b'áttundi': 8, 
   b'áttunda': 8, 
   b'níundi': 9, 
   b'níunda': 9, 
   b'tíundi': 10, 
   b'tíunda': 10, 
   b'ellefti': 11, 
   b'ellefta': 11, 
   b'tólfti': 12, 
   b'tólfta': 12, 
   b'þrettándi': 13, 
   b'þrettánda': 13, 
   b'fjórtándi': 14, 
   b'fjórtánda': 14, 
   b'fimmtándi': 15, 
   b'fimmtánda': 15, 
   b'sextándi': 16, 
   b'sextánda': 16, 
   b'sautjándi': 17, 
   b'sautjánda': 17, 
   b'átjándi': 18, 
   b'átjánda': 18, 
   b'nítjándi': 19, 
   b'nítjánda': 19, 
   b'tuttugasti': 20, 
   b'tuttugasta': 20, 
   b'þrítugasti': 30, 
   b'þrítugasta': 30}
CLOCK_NUMBERS = {b'eitt': [
           1, 0, 0], 
   b'tvö': [
          2, 0, 0], 
   b'þrjú': [
           3, 0, 0], 
   b'fjögur': [
             4, 0, 0], 
   b'fimm': [
           5, 0, 0], 
   b'sex': [
          6, 0, 0], 
   b'sjö': [
          7, 0, 0], 
   b'átta': [
           8, 0, 0], 
   b'níu': [
          9, 0, 0], 
   b'tíu': [
          10, 0, 0], 
   b'ellefu': [
             11, 0, 0], 
   b'tólf': [
           12, 0, 0], 
   b'hálfeitt': [
               12, 30, 0], 
   b'hálftvö': [
              1, 30, 0], 
   b'hálfþrjú': [
               2, 30, 0], 
   b'hálffjögur': [
                 3, 30, 0], 
   b'hálffimm': [
               4, 30, 0], 
   b'hálfsex': [
              5, 30, 0], 
   b'hálfsjö': [
              6, 30, 0], 
   b'hálfátta': [
               7, 30, 0], 
   b'hálfníu': [
              8, 30, 0], 
   b'hálftíu': [
              9, 30, 0], 
   b'hálfellefu': [
                 10, 30, 0], 
   b'hálftólf': [
               11, 30, 0]}
CLOCK_HALF = frozenset([
 b'hálfeitt',
 b'hálftvö',
 b'hálfþrjú',
 b'hálffjögur',
 b'hálffimm',
 b'hálfsex',
 b'hálfsjö',
 b'hálfátta',
 b'hálfníu',
 b'hálftíu',
 b'hálfellefu',
 b'hálftólf'])
CE = frozenset(('e.Kr', 'e.Kr.'))
BCE = frozenset(('f.Kr', 'f.Kr.'))
CE_BCE = CE | BCE
CURRENCY_ABBREV = frozenset(('ISK', 'DKK', 'NOK', 'SEK', 'GBP', 'USD', 'EUR', 'CAD',
                             'AUD', 'CHF', 'JPY', 'PLN', 'RUB', 'CZK', 'INR', 'IDR',
                             'CNY', 'RMB', 'HKD', 'NZD', 'SGD', 'MXN', 'ZAR'))
CURRENCY_SYMBOLS = {b'$': b'USD', 
   b'€': b'EUR', 
   b'£': b'GBP', 
   b'¥': b'JPY', 
   b'₽': b'RUB'}
SINGLECHAR_FRACTIONS = b'↉⅒⅑⅛⅐⅙⅕¼⅓½⅖⅔⅜⅗¾⅘⅝⅚⅞'
SI_UNITS = {b'm²': ('m²', 1.0), 
   b'fm': ('m²', 1.0), 
   b'cm²': ('m²', 0.01), 
   b'm³': ('m³', 1.0), 
   b'cm³': ('m³', 1e-06), 
   b'l': ('m³', 0.001), 
   b'ltr': ('m³', 0.001), 
   b'dl': ('m³', 0.0001), 
   b'cl': ('m³', 1e-05), 
   b'ml': ('m³', 1e-06), 
   b'°C': (
         b'K', lambda x: x + 273.15), 
   b'°F': (
         b'K', lambda x: (x + 459.67) * 5 / 9), 
   b'K': ('K', 1.0), 
   b'g': ('g', 1.0), 
   b'gr': ('g', 1.0), 
   b'kg': ('g', 1000.0), 
   b't': ('g', 1000000.0), 
   b'mg': ('g', 0.001), 
   b'μg': ('g', 1e-06), 
   b'm': ('m', 1.0), 
   b'km': ('m', 1000.0), 
   b'mm': ('m', 0.001), 
   b'μm': ('m', 1e-06), 
   b'cm': ('m', 0.01), 
   b'sm': ('m', 0.01), 
   b's': ('s', 1.0), 
   b'ms': ('s', 0.001), 
   b'μs': ('s', 1e-06), 
   b'Nm': ('J', 1.0), 
   b'klst': ('s', 3600.0), 
   b'mín': ('s', 60.0), 
   b'W': ('W', 1.0), 
   b'mW': ('W', 0.001), 
   b'kW': ('W', 1000.0), 
   b'MW': ('W', 1000000.0), 
   b'GW': ('W', 1000000000.0), 
   b'TW': ('W', 1000000000000.0), 
   b'J': ('J', 1.0), 
   b'kJ': ('J', 1000.0), 
   b'MJ': ('J', 1000000.0), 
   b'GJ': ('J', 1000000000.0), 
   b'TJ': ('J', 1000000000000.0), 
   b'kWh': ('J', 3600000.0), 
   b'MWh': ('J', 3600000000.0), 
   b'kWst': ('J', 3600000.0), 
   b'MWst': ('J', 3600000000.0), 
   b'kcal': ('J', 4184), 
   b'cal': ('J', 4.184), 
   b'N': ('N', 1.0), 
   b'kN': ('N', 1000.0), 
   b'V': ('V', 1.0), 
   b'mV': ('V', 0.001), 
   b'kV': ('V', 1000.0), 
   b'A': ('A', 1.0), 
   b'mA': ('A', 0.001), 
   b'Hz': ('Hz', 1.0), 
   b'kHz': ('Hz', 1000.0), 
   b'MHz': ('Hz', 1000000.0), 
   b'GHz': ('Hz', 1000000000.0), 
   b'Pa': ('Pa', 1.0), 
   b'hPa': ('Pa', 100.0), 
   b'°': ('°', 1.0)}
KLUDGY_ORDINALS_PASS_THROUGH = 0
KLUDGY_ORDINALS_MODIFY = 1
KLUDGY_ORDINALS_TRANSLATE = 2
ORDINAL_ERRORS = {b'1sti': b'fyrsti', 
   b'1sta': b'fyrsta', 
   b'1stu': b'fyrstu', 
   b'3ji': b'þriðji', 
   b'3ju': b'þriðju', 
   b'4ði': b'fjórði', 
   b'4ða': b'fjórða', 
   b'4ðu': b'fjórðu', 
   b'5ti': b'fimmti', 
   b'5ta': b'fimmta', 
   b'5tu': b'fimmtu', 
   b'2svar': b'tvisvar', 
   b'3svar': b'þrisvar', 
   b'2ja': b'tveggja', 
   b'3ja': b'þriggja', 
   b'4ra': b'fjögurra'}
ORDINAL_NUMBERS = {b'1sti': 1, 
   b'1sta': 1, 
   b'1stu': 1, 
   b'3ji': 3, 
   b'3ja': 3, 
   b'3ju': 3, 
   b'4ði': 4, 
   b'4ða': 4, 
   b'4ðu': 4, 
   b'5ti': 5, 
   b'5ta': 5, 
   b'5tu': 5}
RE_ROMAN_NUMERAL = re.compile(b'^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
ROMAN_NUMERAL_MAP = tuple(zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1), ('M',
                                                                                       'CM',
                                                                                       'D',
                                                                                       'CD',
                                                                                       'C',
                                                                                       'XC',
                                                                                       'L',
                                                                                       'XL',
                                                                                       'X',
                                                                                       'IX',
                                                                                       'V',
                                                                                       'IV',
                                                                                       'I')))

def roman_to_int(s):
    """ Quick and dirty conversion of an already validated Roman numeral to integer """
    i = result = 0
    for integer, numeral in ROMAN_NUMERAL_MAP:
        while s[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)

    assert i == len(s)
    return result


MULTIPLIERS = {b'einn': 1, 
   b'tveir': 2, 
   b'þrír': 3, 
   b'fjórir': 4, 
   b'fimm': 5, 
   b'sex': 6, 
   b'sjö': 7, 
   b'átta': 8, 
   b'níu': 9, 
   b'tíu': 10, 
   b'ellefu': 11, 
   b'tólf': 12, 
   b'þrettán': 13, 
   b'fjórtán': 14, 
   b'fimmtán': 15, 
   b'sextán': 16, 
   b'sautján': 17, 
   b'seytján': 17, 
   b'átján': 18, 
   b'nítján': 19, 
   b'tuttugu': 20, 
   b'þrjátíu': 30, 
   b'fjörutíu': 40, 
   b'fimmtíu': 50, 
   b'sextíu': 60, 
   b'sjötíu': 70, 
   b'áttatíu': 80, 
   b'níutíu': 90, 
   b'hundrað': 100, 
   b'þúsund': 1000, 
   b'þús.': 1000, 
   b'milljón': 1000000.0, 
   b'milla': 1000000.0, 
   b'millj.': 1000000.0, 
   b'mljó.': 1000000.0, 
   b'milljarður': 1000000000.0, 
   b'miljarður': 1000000000.0, 
   b'ma.': 1000000000.0, 
   b'mrð.': 1000000000.0}
PERCENTAGES = {b'prósent': 1, b'prósenta': 1, b'hundraðshluti': 1, b'prósentustig': 1}
AMOUNT_ABBREV = {b'kr.': 1, 
   b'kr': 1, 
   b'krónur': 1, 
   b'þ.kr.': 1000.0, 
   b'þ.kr': 1000.0, 
   b'þús.kr.': 1000.0, 
   b'þús.kr': 1000.0, 
   b'm.kr.': 1000000.0, 
   b'm.kr': 1000000.0, 
   b'mkr.': 1000000.0, 
   b'mkr': 1000000.0, 
   b'millj.kr.': 1000000.0, 
   b'millj.kr': 1000000.0, 
   b'mljó.kr.': 1000000.0, 
   b'mljó.kr': 1000000.0, 
   b'ma.kr.': 1000000000.0, 
   b'ma.kr': 1000000000.0, 
   b'mö.kr.': 1000000000.0, 
   b'mö.kr': 1000000000.0, 
   b'mlja.kr.': 1000000000.0, 
   b'mlja.kr': 1000000000.0}
ISK_AMOUNT_PRECEDING = frozenset(('kr.', 'kr', 'krónur'))
URL_PREFIXES = ('http://', 'https://', 'file://')
TOP_LEVEL_DOMAINS = frozenset(('com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'arpa',
                               'eu', 'biz', 'info', 'xyz', 'online', 'site', 'tech',
                               'top', 'space', 'news', 'pro', 'club', 'loan', 'win',
                               'vip', 'icu', 'app', 'blog', 'shop', 'work', 'ltd',
                               'mobi', 'live', 'store', 'gdn', 'ac', 'ad', 'ae',
                               'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as',
                               'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be',
                               'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br',
                               'bs', 'bt', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf',
                               'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr',
                               'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'de', 'dj', 'dk',
                               'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'er', 'es', 'et',
                               'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gd',
                               'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp',
                               'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm',
                               'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in',
                               'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp',
                               'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kw', 'ky',
                               'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt',
                               'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh',
                               'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms',
                               'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc',
                               'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu',
                               'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl',
                               'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're',
                               'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se',
                               'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr',
                               'ss', 'st', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf',
                               'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tr',
                               'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'us', 'uy',
                               'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf',
                               'ws', 'ye', 'yt', 'za', 'zm', 'zw'))
MIN_DOMAIN_LENGTH = 4
DOMAIN_REGEX = re.compile((b'({0})({1}*)$').format((b'|').join([ b'\\w\\.' + d for d in map(re.escape, TOP_LEVEL_DOMAINS) ]), PUNCTUATION_REGEX), re.UNICODE)