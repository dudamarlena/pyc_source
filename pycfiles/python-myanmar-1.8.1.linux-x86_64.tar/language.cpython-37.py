# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trhura/Code/pythonenv/lib/python3.7/site-packages/myanmar/language.py
# Compiled at: 2019-10-01 11:34:23
# Size of source mod 2**32: 6715 bytes
from myanmar import encodings
LETTER_KA = chr(4096)
LETTER_KHA = chr(4097)
LETTER_GA = chr(4098)
LETTER_GHA = chr(4099)
LETTER_NGA = chr(4100)
LETTER_CA = chr(4101)
LETTER_CHA = chr(4102)
LETTER_JA = chr(4103)
LETTER_JHA = chr(4104)
LETTER_NYA = chr(4105)
LETTER_NNYA = chr(4106)
LETTER_TTA = chr(4107)
LETTER_TTHA = chr(4108)
LETTER_DDA = chr(4109)
LETTER_DDHA = chr(4110)
LETTER_NNA = chr(4111)
LETTER_TA = chr(4112)
LETTER_THA = chr(4113)
LETTER_DA = chr(4114)
LETTER_DHA = chr(4115)
LETTER_NA = chr(4116)
LETTER_PA = chr(4117)
LETTER_PHA = chr(4118)
LETTER_BA = chr(4119)
LETTER_BHA = chr(4120)
LETTER_MA = chr(4121)
LETTER_YA = chr(4122)
LETTER_RA = chr(4123)
LETTER_LA = chr(4124)
LETTER_WA = chr(4125)
LETTER_SA = chr(4126)
LETTER_HA = chr(4127)
LETTER_LLA = chr(4128)
LETTER_A = chr(4129)
LETTER_SHAN_A = chr(4130)
LETTER_I = chr(4131)
LETTER_II = chr(4132)
LETTER_U = chr(4133)
LETTER_UU = chr(4134)
LETTER_E = chr(4135)
LETTER_MON_E = chr(4136)
LETTER_O = chr(4137)
LETTER_AU = chr(4138)
VOWEL_SIGN_TALL_AA = chr(4139)
VOWEL_SIGN_AA = chr(4140)
VOWEL_SIGN_I = chr(4141)
VOWEL_SIGN_II = chr(4142)
VOWEL_SIGN_U = chr(4143)
VOWEL_SIGN_UU = chr(4144)
VOWEL_SIGN_E = chr(4145)
VOWEL_SIGN_AI = chr(4146)
VOWEL_SIGN_MON_II = chr(4147)
VOWEL_SIGN_MON_O = chr(4148)
VOWEL_SIGN_E_ABOVE = chr(4149)
SIGN_ANUSVARA = chr(4150)
SIGN_DOT_BELOW = chr(4151)
SIGN_VISARGA = chr(4152)
SIGN_VIRAMA = chr(4153)
SIGN_ASAT = chr(4154)
SIGN_MEDIAL_YA = chr(4155)
SIGN_MEDIAL_RA = chr(4156)
SIGN_MEDIAL_WA = chr(4157)
SIGN_MEDIAL_HA = chr(4158)
LETTER_GREAT_SA = chr(4159)
DIGIT_ZERO = chr(4160)
DIGIT_ONE = chr(4161)
DIGIT_TWO = chr(4162)
DIGIT_THREE = chr(4163)
DIGIT_FOUR = chr(4164)
DIGIT_FIVE = chr(4165)
DIGIT_SIX = chr(4166)
DIGIT_SEVEN = chr(4167)
DIGIT_EIGHT = chr(4168)
DIGIT_NINE = chr(4169)
SIGN_LITTLE_SECTION = chr(4170)
SIGN_SECTION = chr(4171)
SYMBOL_LOCATIVE = chr(4172)
SYMBOL_COMPLETED = chr(4173)
SYMBOL_AFOREMENTIONED = chr(4174)
SYMBOL_GENITIVE = chr(4175)

def ismyanmar(c):
    return c >= LETTER_KA and c <= SYMBOL_GENITIVE


def ismyconsonant(c):
    return c >= LETTER_KA and c <= LETTER_A or c == LETTER_U


def ismymedial(c):
    return c >= SIGN_MEDIAL_YA and c <= SIGN_MEDIAL_HA


def ismyvowel(c):
    return c >= VOWEL_SIGN_TALL_AA and c <= VOWEL_SIGN_AI


def ismytone(c):
    return c == SIGN_DOT_BELOW or c == SIGN_VISARGA


def ismydigit(c):
    return c >= DIGIT_ZERO and c <= DIGIT_NINE


def ismypunct(c):
    return c == SIGN_LITTLE_SECTION or c == SIGN_SECTION


def ismydiac(c):
    return ismyvowel(c) or ismymedial(c) or ismytone(c) or c == SIGN_ANUSVARA or c == SIGN_ASAT


def ismyindependvowel(c):
    return c >= LETTER_I and c <= LETTER_E or c == LETTER_O or c == LETTER_AU


def ismyindependsymbol(c):
    return c >= SYMBOL_LOCATIVE and c <= SYMBOL_GENITIVE


def ismyletter(c):
    return ismyconsonant(c) or ismyindependvowel(c) or c == SYMBOL_AFOREMENTIONED


def ismymark(c):
    return ismymedial(c) or ismyvowel(c) or c >= SIGN_ANUSVARA and c <= SIGN_ASAT


def MorphoSyllableBreak(text, encoding):
    """
    Return an iterable of morphological / visual syllables in text.

    >>> from myanmar.encodings import UnicodeEncoding
    >>> slb = list(MorphoSyllableBreak("အကြွေးပေး", UnicodeEncoding()))
    >>> list(s['syllable'] for s in slb)
    ['အ', 'ကြွေး', 'ပေး']
    >>> slb[2]
    {'syllable': 'ပေး', 'consonant': 'ပ', 'eVowel': 'ေ', 'visarga': 'း'}
    """
    if not isinstance(encoding, encodings.BaseEncoding):
        raise TypeError(encoding + 'is not a valid encoding')
    start = 0
    while start < len(text):
        match = encoding.morphologic_pattern.search(text, start)
        if not match:
            syllable = {'syllable': text[start:]}
            start = len(text)
        else:
            if start < match.start():
                syllable = {'syllable': text[start:match.start()]}
                start = match.start()
            else:
                syllable = {k:v for k, v in match.groupdict().items() if v if v}
                start = match.end()
        yield syllable


def PhonemicSyllableBreak(text, encoding):
    """
    Return an iterable of phonemic syllables in text.

    >>> from myanmar.encodings import UnicodeEncoding
    >>> slb = list(PhonemicSyllableBreak("သီးပင်အိုင်", UnicodeEncoding()))
    >>> list(s['syllable'] for s in slb)
    ['သီး', 'ပင်', 'အိုင်']
    >>> slb[0]
    {'syllable': 'သီး', 'consonant': 'သ', 'iVowel': 'ီ', 'visarga': 'း'}
    """
    if not isinstance(encoding, encodings.BaseEncoding):
        raise TypeError(encoding + 'is not a valid encoding')
    start = 0
    while start < len(text):
        match = encoding.phonemic_pattern.search(text, start)
        if not match:
            syllable = {'syllable': text[start:]}
            start = len(text)
        else:
            if start < match.start():
                syllable = {'syllable': text[start:match.start()]}
                start = match.start()
            else:
                syllable = {k:v for k, v in match.groupdict().items() if v if v}
                start = match.end()
        yield syllable