# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/t/work/cihai/cihai/cihai/conversion.py
# Compiled at: 2019-08-18 05:27:00
# Size of source mod 2**32: 7937 bytes
__doc__ = 'Conversion functions for various CJK encodings and representations.\n\nNotes\n-----\nOriginal methods and docs based upon `ltchinese`_, license `MIT`_ Steven\nKryskalla.\n\n.. versionadded:: 0.1\n    Python 2/3 compatibility.\n\n    - PEP8, PEP257.\n    - ``int()`` casting for comparisons\n    - Python 3 support.\n    - Python 3 fix for :meth:`~.ucn_to_python`.\n    - Python 3 ``__future__`` statements.\n    - All methods converting to ``_python`` will return ``Unicode``.\n    - All methods converting Unicode to x will return bytestring.\n    - Add :meth:`~.ucnstring_to_python`\n    - Any other change upon @ `conversion.py @9227813`_.\n\nThe following terms are used to represent the encodings / representation used\nin the conversion functions (the samples on the right are for the character\nU+4E00 (yi1; "one")):\n\n========================== ====================================================\nGB2312 (Kuten/Quwei form)  "5027" [used in the "GB2312" field of Unihan.txt]\nGB2312 (ISO-2022 form)     "523B" [the "internal representation" of GB code]\nEUC-CN                     "D2BB" [this is the "external encoding" of GB2312-\n                                    ISO2022\'s "internal representation"; also\n                                    the form that Ocrat uses]\nUTF-8                      "E4 B8 80" [used in the "UTF-8" field in Unihan.txt]\n-------------------------- ----------------------------------------------------\nUnihan UCN                 "U+4E00"   [used by Unicode Inc.]\n-------------------------- ----------------------------------------------------\ninternal Python unicode    u"一"  [this is the most useful form!]\ninternal Python \'utf8\'     "\\xe4\\xb8\\x80"\ninternal Python \'gb2312\'   "\\xd2\\xbb"\ninternal Python \'euc-cn\'   "\\xd2\\xbb"\ninternal Python \'gb18030\'  "\\xd2\\xbb"\n========================== ====================================================\n\nSee these resources for more information:\n * Wikipedia "Extended_Unix_Code" article\n\n   * "EUC-CN is the usual way to use the GB2312 standard for simplified Chinese\n     characters ... the ISO-2022 form of GB2312 is not normally used"\n\n * Wikipedia "HZ_(encoding)" article (the example conversion)\n\n * Wikipedia "Numeric_character_reference" article\n\n * Unihan (look for "Encoding forms", "Mappings to Major Standards")\n\n   * e.g. http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=4E00\n\n.. _ltchinese: https://bitbucket.org/lost_theory/ltchinese\n.. _MIT: https://bitbucket.org/lost_theory/ltchinese/src/9227813/LICENSE.txt\n.. _conversion.py @9227813: https://bitbucket.org/lost_theory/ltchinese/raw/9227813/ltchinese/conversion.py\n'
from __future__ import absolute_import, print_function, unicode_literals
import logging, re
from ._compat import string_types, text_type, unichr
log = logging.getLogger(__name__)

def hexd(n):
    """Return hex digits (strip '0x' at the beginning)."""
    return hex(n)[2:]


def kuten_to_gb2312(kuten):
    """
    Convert GB kuten / quwei form (94 zones * 94 points) to GB2312-1980 /
    ISO-2022-CN hex (internal representation)
    """
    zone, point = int(kuten[:2]), int(kuten[2:])
    hi, lo = hexd(zone + 32), hexd(point + 32)
    gb2312 = '%s%s' % (hi, lo)
    assert isinstance(gb2312, bytes)
    return gb2312


def gb2312_to_euc(gb2312hex):
    """
    Convert GB2312-1980 hex (internal representation) to EUC-CN hex (the
    "external encoding")
    """
    hi, lo = int(gb2312hex[:2], 16), int(gb2312hex[2:], 16)
    hi, lo = hexd(hi + 128), hexd(lo + 128)
    euc = '%s%s' % (hi, lo)
    assert isinstance(euc, bytes)
    return euc


def euc_to_python(hexstr):
    """
    Convert a EUC-CN (GB2312) hex to a Python unicode string.
    """
    hi = hexstr[0:2]
    lo = hexstr[2:4]
    gb_enc = '\\x' + hi + '\\x' + lo
    return gb_enc.decode('gb2312')


def euc_to_utf8(euchex):
    """
    Convert EUC hex (e.g. "d2bb") to UTF8 hex (e.g. "e4 b8 80").
    """
    utf8 = euc_to_python(euchex).encode('utf-8')
    uf8 = utf8.decode('unicode_escape')
    uf8 = uf8.encode('latin1')
    uf8 = uf8.decode('euc-jp')
    return uf8


def ucn_to_unicode(ucn):
    r"""
    Convert a Unicode Universal Character Number (e.g. "U+4E00" or "4E00") to
    Python unicode (u'\u4e00')
    """
    if isinstance(ucn, string_types):
        ucn = ucn.strip('U+')
        if len(ucn) > int(4):
            char = '\\U' + format(int(ucn, 16), '08x').encode('latin1')
            char = char.decode('unicode_escape')
        else:
            char = unichr(int(ucn, 16))
    else:
        char = unichr(ucn)
    assert isinstance(char, text_type)
    return char


def euc_to_unicode(hexstr):
    r"""
    Return EUC-CN (GB2312) hex to a Python unicode.

    Parameters
    ----------
    hexstr : bytes

    Returns
    -------
    unicode :
        Python unicode  e.g. ``u'\u4e00'`` / '一'.

    Examples
    --------

    >>> u'一'.encode('gb2312').decode('utf-8')
    u'һ'

    >>> (b'\x' + b'd2' + b'\x' + b'bb').replace('\x', '') \
    ... .decode('hex').decode('utf-8')
    u'һ'

    Note: bytes don't have a ``.replace``:

    >>> gb_enc = gb_enc.replace('\x', '').decode('hex')
    >>> gb_enc.decode('string_escape')  # Won't work with Python 3.x.
    """
    hi = hexstr[0:2]
    lo = hexstr[2:4]
    gb_enc = '\\x' + hi + '\\x' + lo
    assert isinstance(gb_enc, bytes)
    gb_enc = gb_enc.decode('unicode_escape')
    gb_enc = gb_enc.encode('latin1')
    gb_enc = gb_enc.decode('gb2312')
    assert isinstance(gb_enc, text_type)
    return gb_enc


def python_to_ucn(uni_char, as_bytes=False):
    r"""
    Return UCN character from Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\u4e00') to the
    corresponding Unicode UCN ('U+4E00').
    """
    ucn = uni_char.encode('unicode_escape').decode('latin1')
    ucn = text_type(ucn).replace('\\', '').upper().lstrip('U')
    if len(ucn) > int(4):
        ucn = ucn.lstrip('0')
    ucn = 'U+' + ucn.upper()
    if as_bytes:
        ucn = ucn.encode('latin1')
    return ucn


def python_to_euc(uni_char, as_bytes=False):
    r"""
    Return EUC character from a Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\u4e00') to the
    corresponding EUC hex ('d2bb').
    """
    euc = repr(uni_char.encode('gb2312'))[1:-1].replace('\\x', '').strip("'")
    if as_bytes:
        euc = euc.encode('utf-8')
        assert isinstance(euc, bytes)
    return euc


def ucnstring_to_unicode(ucn_string):
    """Return ucnstring as Unicode."""
    ucn_string = ucnstring_to_python(ucn_string).decode('utf-8')
    assert isinstance(ucn_string, text_type)
    return ucn_string


def ucnstring_to_python(ucn_string):
    r"""
    Return string with Unicode UCN (e.g. "U+4E00") to native Python Unicode
    (u'\u4e00').
    """
    res = re.findall('U\\+[0-9a-fA-F]*', ucn_string)
    for r in res:
        ucn_string = ucn_string.replace(text_type(r), text_type(ucn_to_unicode(r)))

    ucn_string = ucn_string.encode('utf-8')
    assert isinstance(ucn_string, bytes)
    return ucn_string


def parse_var(var):
    """
    Returns a tuple consisting of a string and a tag, or None, if none is
    specified.
    """
    bits = var.split('<', 1)
    if len(bits) < 2:
        tag = None
    else:
        tag = bits[1]
    return (ucn_to_unicode(bits[0]), tag)


def parse_vars(_vars):
    """
    Return an iterator of (char, tag) tuples.
    """
    for var in _vars.split(' '):
        yield parse_var(var)


def parse_untagged(_vars):
    """
    Return an iterator of chars.
    """
    return (char for char, _tag in parse_vars(_vars))