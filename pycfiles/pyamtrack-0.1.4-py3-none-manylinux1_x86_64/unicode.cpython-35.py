# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/unicode.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 9433 bytes
__doc__ = 'PyAMS_utils.unicode module\n\nThis module provides a small set of functions which can be used to handle unicode data and\ntheir bytes equivalent.\n'
import codecs, string
__docformat__ = 'restructuredtext'
_UNICODE_TRANS_TABLE = {}

def _fill_unicode_trans_table():
    _corresp = [
     (
      'A', [192, 193, 194, 195, 196, 197, 256, 258, 260]),
     (
      'AE', [198]),
     (
      'a', [224, 225, 226, 227, 228, 229, 257, 259, 261]),
     (
      'ae', [230]),
     (
      'C', [199, 262, 264, 266, 268]),
     (
      'c', [231, 263, 265, 267, 269]),
     (
      'D', [208, 270, 272]),
     (
      'd', [240, 271, 273]),
     (
      'E', [200, 201, 202, 203, 274, 276, 278, 280, 282]),
     (
      'e', [232, 233, 234, 235, 275, 277, 279, 281, 283]),
     (
      'G', [284, 286, 288, 290]),
     (
      'g', [285, 287, 289, 291]),
     (
      'H', [292, 294]),
     (
      'h', [293, 295]),
     (
      'I', [204, 205, 206, 207, 296, 298, 300, 302, 304]),
     (
      'i', [236, 237, 238, 239, 297, 299, 301, 303, 305]),
     (
      'IJ', [306]),
     (
      'ij', [307]),
     (
      'J', [308]),
     (
      'j', [309]),
     (
      'K', [310]),
     (
      'k', [311, 312]),
     (
      'L', [313, 315, 317, 319, 321]),
     (
      'l', [314, 316, 318, 320, 322]),
     (
      'N', [209, 323, 325, 327, 330]),
     (
      'n', [241, 324, 326, 328, 329, 331]),
     (
      'O', [210, 211, 212, 213, 214, 216, 332, 334, 336]),
     (
      'o', [176, 242, 243, 244, 245, 246, 248, 333, 335, 337]),
     (
      'OE', [338]),
     (
      'oe', [339]),
     (
      'R', [340, 342, 344]),
     (
      'r', [341, 343, 345]),
     (
      'S', [346, 348, 350, 352]),
     (
      's', [347, 349, 351, 5648, 383]),
     (
      'T', [354, 356, 358]),
     (
      't', [355, 357, 359]),
     (
      'U', [217, 218, 219, 220, 360, 362, 364, 366, 368, 370]),
     (
      'u', [249, 250, 251, 252, 361, 363, 365, 367, 369]),
     (
      'W', [372]),
     (
      'w', [373]),
     (
      'Y', [221, 374, 376]),
     (
      'y', [253, 255, 375]),
     (
      'Z', [377, 379, 381]),
     (
      'z', [378, 380, 382]),
     (
      "'", [8217])]
    for char, codes in _corresp:
        for code in codes:
            _UNICODE_TRANS_TABLE[code] = char


_fill_unicode_trans_table()
_REMOVED_CHARS = '®©™…'

def translate_string(value, escape_slashes=False, force_lower=True, spaces=' ', remove_punctuation=True, keep_chars='_-.'):
    """Remove extended characters and diacritics from string and replace them with 'basic' ones

    :param str value: text to be translated
    :param boolean escape_slashes: if True, slashes are also converted
    :param boolean force_lower: if True, result is automatically converted to lower case
    :param str spaces: character used to replace spaces
    :param boolean remove_punctuation: if True, all punctuation characters are removed
    :param str keep_chars: characters which may be kept in the input string
    :return: text without diacritics or special characters

    >>> from pyams_utils.unicode import translate_string
    >>> input_string = 'Ceci est un test en Français !!!'
    >>> translate_string(input_string)
    'ceci est un test en francais'
    >>> translate_string(input_string, force_lower=False)
    'Ceci est un test en Francais'
    >>> translate_string(input_string, spaces='-')
    'ceci-est-un-test-en-francais'
    >>> translate_string(input_string, remove_punctuation=False)
    'ceci est un test en francais !!!'
    >>> translate_string(input_string, keep_chars='!')
    'ceci est un test en francais !!!'
    """
    if escape_slashes:
        value = value.replace('\\', '/').split('/')[(-1)]
    value = value.strip()
    if isinstance(value, bytes):
        value = value.decode('utf-8', 'replace')
    value = value.translate(_UNICODE_TRANS_TABLE)
    if remove_punctuation:
        punctuation = ''.join(filter(lambda x: x not in keep_chars, string.punctuation + _REMOVED_CHARS))
        value = ''.join(filter(lambda x: x not in punctuation, value))
    if force_lower:
        value = value.lower()
    value = value.strip()
    if spaces != ' ':
        value = value.replace(' ', spaces)
    return value


def nvl(value, default=''):
    """Get specified value, or an empty string if value is empty

    :param object value: value to be checked
    :param object default: default value to be returned if value is *false*
    :return: input value, or *default* if value is *false*

    >>> from pyams_utils.unicode import nvl
    >>> nvl(None)
    ''
    >>> nvl('foo')
    'foo'
    >>> nvl(False, 'bar')
    'bar'
    """
    return value or default


def uninvl(value, default='', encoding='utf-8'):
    r"""Get specified value converted to unicode, or an empty unicode string if value is empty

    :param str/bytes value: the input to be checked
    :param default: str; default value
    :param encoding: str; encoding name to use for conversion
    :return: str; value, or *default* if value is empty, converted to unicode

    >>> from pyams_utils.unicode import uninvl
    >>> uninvl('String value')
    'String value'
    >>> uninvl(b'String value')
    'String value'
    >>> uninvl(b'Cha\xc3\xaene accentu\xc3\xa9e')
    'Chaîne accentuée'
    >>> uninvl(b'Cha\xeene accentu\xe9e', 'latin1')
    'Chaîne accentuée'
    """
    if isinstance(value, str):
        return value
        try:
            return codecs.decode(value or default, encoding)
        except ValueError:
            return codecs.decode(value or default, 'latin1')


def unidict(value, encoding='utf-8'):
    r"""Get specified dict with values converted to unicode

    :param dict value: input mapping of strings which may be converted to unicode
    :param str encoding: output encoding
    :return: dict; a new mapping with each value converted to unicode

    >>> from pyams_utils.unicode import unidict
    >>> unidict({'input': b'Cha\xc3\xaene accentu\xc3\xa9e'})
    {'input': 'Chaîne accentuée'}
    >>> unidict({'input': b'Cha\xeene accentu\xe9e'}, 'latin1')
    {'input': 'Chaîne accentuée'}
    """
    result = {}
    for key in value:
        result[key] = uninvl(value[key], encoding)

    return result


def unilist(value, encoding='utf-8'):
    r"""Get specified list with values converted to unicode

    :param list value: input list of strings which may be converted to unicode
    :param str encoding: output encoding
    :return: list; a new list with each value converted to unicode

    >>> from pyams_utils.unicode import unilist
    >>> unilist([b'Cha\xc3\xaene accentu\xc3\xa9e'])
    ['Chaîne accentuée']
    >>> unilist([b'Cha\xeene accentu\xe9e'], 'latin1')
    ['Chaîne accentuée']
    """
    if not isinstance(value, (list, tuple)):
        return uninvl(value, encoding)
    return [uninvl(v, encoding) for v in value]


def encode(value, encoding='utf-8'):
    r"""Encode given Unicode value to bytes with given encoding

    :param str value: the value to encode
    :param str encoding: selected encoding
    :return: bytes; value encoded to bytes if input is a string, original value otherwise

    >>> from pyams_utils.unicode import encode
    >>> encode('Chaîne accentuée')
    b'Cha\xc3\xaene accentu\xc3\xa9e'
    >>> encode('Chaîne accentuée', 'latin1')
    b'Cha\xeene accentu\xe9e'
    """
    if isinstance(value, str):
        return value.encode(encoding)
    return value


def utf8(value):
    r"""Encode given unicode value to UTF-8 encoded bytes

    :param str value: the value to encode to utf-8
    :return: bytes; value encoded to bytes if input is a string, original value otherwise

    >>> from pyams_utils.unicode import utf8
    >>> utf8('Chaîne accentuée')
    b'Cha\xc3\xaene accentu\xc3\xa9e'
    """
    return encode(value, 'utf-8')


def decode(value, encoding='utf-8'):
    r"""Decode given bytes value to unicode with given encoding

    :param bytes value: the value to decode
    :param str encoding: selected encoding
    :return: str; value decoded to unicode string if input is a bytes, original value otherwise

    >>> from pyams_utils.unicode import decode
    >>> decode(b'Cha\xc3\xaene accentu\xc3\xa9e')
    'Chaîne accentuée'
    >>> decode(b'Cha\xeene accentu\xe9e', 'latin1')
    'Chaîne accentuée'
    """
    if isinstance(value, bytes):
        return value.decode(encoding)
    return value