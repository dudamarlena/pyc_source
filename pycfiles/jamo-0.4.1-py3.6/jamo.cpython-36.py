# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/jamo/jamo.py
# Compiled at: 2017-11-06 14:27:03
# Size of source mod 2**32: 9914 bytes
"""Syllable and jamo analysis for Korean. Default internal exchange form is
Hangul characters, not codepoints. Jamo exchange form is U+11xx characters,
not U+3xxx Hangul Compatibility Jamo (HCJ) characters or codepoints.

For more information, see:
http://python-jamo.readthedocs.org/ko/latest/
"""
import os
from sys import stderr
from itertools import chain
import json, re
_ROOT = os.path.abspath(os.path.dirname(__file__))
_JAMO_OFFSET = 44032
_JAMO_LEAD_OFFSET = 4351
_JAMO_VOWEL_OFFSET = 4448
_JAMO_TAIL_OFFSET = 4519
with open(os.path.join(_ROOT, 'data', 'U+11xx.json'), 'r') as (namedata):
    _JAMO_TO_NAME = json.load(namedata)
_JAMO_REVERSE_LOOKUP = {name:char for char, name in _JAMO_TO_NAME.items()}
with open(os.path.join(_ROOT, 'data', 'U+31xx.json'), 'r') as (namedata):
    _HCJ_TO_NAME = json.load(namedata)
_HCJ_REVERSE_LOOKUP = {name:char for char, name in _HCJ_TO_NAME.items()}
JAMO_LEADS = [chr(_) for _ in range(4352, 4447)]
JAMO_LEADS_MODERN = [chr(_) for _ in range(4352, 4371)]
JAMO_VOWELS = [chr(_) for _ in range(4449, 4520)]
JAMO_VOWELS_MODERN = [chr(_) for _ in range(4449, 4470)]
JAMO_TAILS = [chr(_) for _ in range(4520, 4608)]
JAMO_TAILS_MODERN = [chr(_) for _ in range(4520, 4547)]

class InvalidJamoError(Exception):
    __doc__ = 'jamo is a U+11xx codepoint.'

    def __init__(self, message, jamo):
        super(InvalidJamoError, self).__init__(message)
        self.jamo = hex(ord(jamo))
        print('Could not parse jamo: U+{code}'.format(code=(self.jamo[2:])), file=stderr)


def _hangul_char_to_jamo(syllable):
    """Return a 3-tuple of lead, vowel, and tail jamo characters.
    Note: Non-Hangul characters are echoed back.
    """
    if is_hangul_char(syllable):
        rem = ord(syllable) - _JAMO_OFFSET
        tail = rem % 28
        vowel = 1 + (rem - tail) % 588 // 28
        lead = 1 + rem // 588
        if tail:
            return (chr(lead + _JAMO_LEAD_OFFSET),
             chr(vowel + _JAMO_VOWEL_OFFSET),
             chr(tail + _JAMO_TAIL_OFFSET))
        else:
            return (
             chr(lead + _JAMO_LEAD_OFFSET),
             chr(vowel + _JAMO_VOWEL_OFFSET))
    else:
        return syllable


def _jamo_to_hangul_char(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo characters.
    """
    lead = ord(lead) - _JAMO_LEAD_OFFSET
    vowel = ord(vowel) - _JAMO_VOWEL_OFFSET
    tail = ord(tail) - _JAMO_TAIL_OFFSET if tail else 0
    return chr(tail + (vowel - 1) * 28 + (lead - 1) * 588 + _JAMO_OFFSET)


def _jamo_char_to_hcj(char):
    if is_jamo(char):
        hcj_name = re.sub('(?<=HANGUL )(\\w+)', 'LETTER', _get_unicode_name(char))
        if hcj_name in _HCJ_REVERSE_LOOKUP.keys():
            return _HCJ_REVERSE_LOOKUP[hcj_name]
    return char


def _get_unicode_name(char):
    """Fetch the unicode name for jamo characters.
    """
    if char not in _JAMO_TO_NAME.keys():
        if char not in _HCJ_TO_NAME.keys():
            raise InvalidJamoError('Not jamo or nameless jamo character', char)
    else:
        if is_hcj(char):
            return _HCJ_TO_NAME[char]
        else:
            return _JAMO_TO_NAME[char]


def is_jamo(character):
    """Test if a single character is a jamo character.
    Valid jamo includes all modern and archaic jamo, as well as all HCJ.
    Non-assigned code points are invalid.
    """
    code = ord(character)
    return 4352 <= code <= 4607 or 43360 <= code <= 43388 or 55216 <= code <= 55238 or 55243 <= code <= 55291 or is_hcj(character)


def is_jamo_modern(character):
    """Test if a single character is a modern jamo character.
    Modern jamo includes all U+11xx jamo in addition to HCJ in modern usage,
    as defined in Unicode 7.0.
    WARNING: U+1160 is NOT considered a modern jamo character, but it is listed
    under 'Medial Vowels' in the Unicode 7.0 spec.
    """
    code = ord(character)
    return 4352 <= code <= 4370 or 4449 <= code <= 4469 or 4520 <= code <= 4546 or is_hcj_modern(character)


def is_hcj(character):
    """Test if a single character is a HCJ character.
    HCJ is defined as the U+313x to U+318x block, sans two non-assigned code
    points.
    """
    return 12593 <= ord(character) <= 12686 and ord(character) != 12644


def is_hcj_modern(character):
    """Test if a single character is a modern HCJ character.
    Modern HCJ is defined as HCJ that corresponds to a U+11xx jamo character
    in modern usage.
    """
    code = ord(character)
    return 12593 <= code <= 12622 or 12623 <= code <= 12643


def is_hangul_char(character):
    """Test if a single character is in the U+AC00 to U+D7A3 code block,
    excluding unassigned codes.
    """
    return 44032 <= ord(character) <= 55203


def get_jamo_class(jamo):
    """Determine if a jamo character is a lead, vowel, or tail.
    Integers and U+11xx characters are valid arguments. HCJ consonants are not
    valid here.

    get_jamo_class should return the class ["lead" | "vowel" | "tail"] of a
    given character or integer.

    Note: jamo class directly corresponds to the Unicode 7.0 specification,
    thus includes filler characters as having a class.
    """
    if jamo in JAMO_LEADS or jamo == chr(4447):
        return 'lead'
    else:
        if not jamo in JAMO_VOWELS:
            if not jamo == chr(4448):
                if 12623 <= ord(jamo) <= 12643:
                    return 'vowel'
        if jamo in JAMO_TAILS:
            return 'tail'
    raise InvalidJamoError('Invalid or classless jamo argument.', jamo)


def jamo_to_hcj(data):
    """Convert jamo to HCJ.
    Arguments may be iterables or single characters.

    jamo_to_hcj should convert every jamo character into HCJ in a given input,
    if possible. Anything else is unchanged.

    jamo_to_hcj is the generator version of j2hcj, the string version. Passing
    a character to jamo_to_hcj will still return a generator.
    """
    return (_jamo_char_to_hcj(_) for _ in data)


def j2hcj(jamo):
    """Convert jamo into HCJ.
    Arguments may be iterables or single characters.

    j2hcj should convert every jamo character into HCJ in a given input, if
    possible. Anything else is unchanged.

    j2hcj is the string version of jamo_to_hcj, the generator version.
    """
    return ''.join(jamo_to_hcj(jamo))


def hcj_to_jamo(hcj_char, position='vowel'):
    """Convert a HCJ character to a jamo character.
    Arguments may be single characters along with the desired jamo class
    (lead, vowel, tail). Non-mappable input will raise an InvalidJamoError.
    """
    if position == 'lead':
        jamo_class = 'CHOSEONG'
    else:
        if position == 'vowel':
            jamo_class = 'JUNGSEONG'
        else:
            if position == 'tail':
                jamo_class = 'JONGSEONG'
            else:
                raise InvalidJamoError('No mapping from input to jamo.', hcj_char)
    jamo_name = re.sub('(?<=HANGUL )(\\w+)', jamo_class, _get_unicode_name(hcj_char))
    if jamo_name in _JAMO_REVERSE_LOOKUP.keys():
        return _JAMO_REVERSE_LOOKUP[jamo_name]
    else:
        return hcj_char


def hcj2j(hcj_char, position='vowel'):
    """Convert a HCJ character to a jamo character.
    Identical to hcj_to_jamo.
    """
    return hcj_to_jamo(hcj_char, position)


def hangul_to_jamo(hangul_string):
    """Convert a string of Hangul to jamo.
    Arguments may be iterables of characters.

    hangul_to_jamo should split every Hangul character into U+11xx jamo
    characters for any given string. Non-hangul characters are not changed.

    hangul_to_jamo is the generator version of h2j, the string version.
    """
    return (_ for _ in chain.from_iterable(_hangul_char_to_jamo(_) for _ in hangul_string))


def h2j(hangul_string):
    """Convert a string of Hangul to jamo.
    Arguments may be iterables of characters.

    h2j should split every Hangul character into U+11xx jamo for any given
    string. Non-hangul characters are not touched.

    h2j is the string version of hangul_to_jamo, the generator version.
    """
    return ''.join(hangul_to_jamo(hangul_string))


def jamo_to_hangul(lead, vowel, tail=''):
    """Return the Hangul character for the given jamo input.
    Integers corresponding to U+11xx jamo codepoints, U+11xx jamo characters,
    or HCJ are valid inputs.

    Outputs a one-character Hangul string.

    This function is identical to j2h.
    """
    lead = hcj_to_jamo(lead, 'lead')
    vowel = hcj_to_jamo(vowel, 'vowel')
    if not tail or ord(tail) == 0:
        tail = None
    else:
        if is_hcj(tail):
            tail = hcj_to_jamo(tail, 'tail')
    if is_jamo(lead):
        if get_jamo_class(lead) == 'lead':
            if is_jamo(vowel):
                if get_jamo_class(vowel) == 'vowel':
                    if not tail or is_jamo(tail) and get_jamo_class(tail) == 'tail':
                        result = _jamo_to_hangul_char(lead, vowel, tail)
                        if is_hangul_char(result):
                            return result
    raise InvalidJamoError('Could not synthesize characters to Hangul.', '\x00')


def j2h(lead, vowel, tail=0):
    """Arguments may be integers corresponding to the U+11xx codepoints, the
    actual U+11xx jamo characters, or HCJ.

    Outputs a one-character Hangul string.

    This function is defined solely for naming conisistency with
    jamo_to_hangul.
    """
    return jamo_to_hangul(lead, vowel, tail)


def synth_hangul(string):
    """Convert jamo characters in a string into hcj as much as possible."""
    raise NotImplementedError
    return ''.join([''.join(''.join(jamo_to_hcj(_)) for _ in string)])