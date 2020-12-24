# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/unicodeutil/hangulutil.py
# Compiled at: 2018-05-03 01:07:20
# Size of source mod 2**32: 10286 bytes
import codecs, os, six
_hangul_syllable_types = {}
_jamo_short_names = {}

def _load_hangul_syllable_types():
    """
    Helper function for parsing the contents of "HangulSyllableType.txt" from the Unicode Character Database (UCD) and
    generating a lookup table for determining whether or not a given Hangul syllable is of type "L", "V", "T", "LV" or
    "LVT".  For more info on the UCD, see the following website: https://www.unicode.org/ucd/
    """
    filename = 'HangulSyllableType.txt'
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with codecs.open((os.path.join(current_dir, filename)), mode='r', encoding='utf-8') as (fp):
        for line in fp:
            if line.strip():
                if line.startswith('#'):
                    pass
                else:
                    data = line.strip().split(';')
                    syllable_type, _ = map(six.text_type.strip, data[1].split('#'))
                    if '..' in data[0]:
                        start, end = map(lambda x: int(x, 16), data[0].strip().split('..'))
                        for idx in range(start, end + 1):
                            _hangul_syllable_types[idx] = syllable_type

                    else:
                        _hangul_syllable_types[int(data[0].strip(), 16)] = syllable_type


def _load_jamo_short_names():
    """
    Function for parsing the Jamo short names from the Unicode Character Database (UCD) and generating a lookup table
    For more info on how this is used, see the Unicode Standard, ch. 03, section 3.12, "Conjoining Jamo Behavior" and
    ch. 04, section 4.8, "Name".

    https://www.unicode.org/versions/latest/ch03.pdf
    https://www.unicode.org/versions/latest/ch04.pdf
    """
    filename = 'Jamo.txt'
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with codecs.open((os.path.join(current_dir, filename)), mode='r', encoding='utf-8') as (fp):
        for line in fp:
            if line.strip():
                if line.startswith('#'):
                    pass
                else:
                    data = line.strip().split(';')
                    code = int(data[0].strip(), 16)
                    char_info = data[1].split('#')
                    short_name = char_info[0].strip()
                    _jamo_short_names[code] = short_name


def _is_hangul_syllable(i):
    """
    Function for determining if a Unicode scalar value i is within the range of Hangul syllables.

    :param i: Unicode scalar value to lookup
    :return: Boolean: True if the lookup value is within the range of Hangul syllables, otherwise False.
    """
    if i in range(44032, 55204):
        return True
    return False


def _is_jamo(i):
    """
    Function for determining if a Unicode scalar value i is within the range of Jamo.

    :param i: Unicode scalar value to lookup
    :return: Boolean: True if the lookup value is within the range of Hangul syllables, otherwise False.
    """
    if i in range(4352, 4608):
        return True
    return False


def _get_hangul_syllable_type(hangul_syllable):
    """
    Function for taking a Unicode scalar value representing a Hangul syllable and determining the correct value for its
    Hangul_Syllable_Type property.  For more information on the Hangul_Syllable_Type property see the Unicode Standard,
    ch. 03, section 3.12, Conjoining Jamo Behavior.

    https://www.unicode.org/versions/latest/ch03.pdf

    :param hangul_syllable: Unicode scalar value representing a Hangul syllable
    :return: Returns a string representing its Hangul_Syllable_Type property ("L", "V", "T", "LV" or "LVT")
    """
    if not _is_hangul_syllable(hangul_syllable):
        raise ValueError('Value 0x%0.4x does not represent a Hangul syllable!' % hangul_syllable)
    if not _hangul_syllable_types:
        _load_hangul_syllable_types()
    return _hangul_syllable_types[hangul_syllable]


def _get_jamo_short_name(jamo):
    """
    Function for taking a Unicode scalar value representing a Jamo and determining the correct value for its
    Jamo_Short_Name property.  For more information on the Jamo_Short_Name property see the Unicode Standard,
    ch. 03, section 3.12, Conjoining Jamo Behavior.

    https://www.unicode.org/versions/latest/ch03.pdf

    :param jamo: Unicode scalar value representing a Jamo
    :return: Returns a string representing its Jamo_Short_Name property
    """
    if not _is_jamo(jamo):
        raise ValueError('Value 0x%0.4x passed in does not represent a Jamo!' % jamo)
    if not _jamo_short_names:
        _load_jamo_short_names()
    return _jamo_short_names[jamo]


S_BASE = 44032
L_BASE = 4352
V_BASE = 4449
T_BASE = 4519
L_COUNT = 19
V_COUNT = 21
T_COUNT = 28
N_COUNT = V_COUNT * T_COUNT
S_COUNT = L_COUNT * N_COUNT

def compose_hangul_syllable(jamo):
    """
    Function for taking a tuple or list of Unicode scalar values representing Jamo and composing it into a Hangul
    syllable.  If the values in the list or tuple passed in are not in the ranges of Jamo, a ValueError will be raised.

    The algorithm for doing the composition is described in the Unicode Standard, ch. 03, section 3.12, "Conjoining Jamo
    Behavior."

    Example: (U+1111, U+1171) -> U+D4CC
             (U+D4CC, U+11B6) -> U+D4DB
             (U+1111, U+1171, U+11B6) -> U+D4DB

    :param jamo: Tuple of list of Jamo to compose
    :return: Composed Hangul syllable
    """
    fmt_str_invalid_sequence = '{0} does not represent a valid sequence of Jamo!'
    if len(jamo) == 3:
        l_part, v_part, t_part = jamo
        if l_part in range(4352, 4371):
            if not (v_part in range(4449, 4470) and t_part in range(4520, 4547)):
                raise ValueError(fmt_str_invalid_sequence.format(jamo))
    else:
        l_index = l_part - L_BASE
        v_index = v_part - V_BASE
        t_index = t_part - T_BASE
        lv_index = l_index * N_COUNT + v_index * T_COUNT
        return S_BASE + lv_index + t_index
        if len(jamo) == 2:
            if jamo[0] in range(4352, 4371):
                if jamo[1] in range(4449, 4470):
                    l_part, v_part = jamo
                    l_index = l_part - L_BASE
                    v_index = v_part - V_BASE
                    lv_index = l_index * N_COUNT + v_index * T_COUNT
                    return S_BASE + lv_index
            if _get_hangul_syllable_type(jamo[0]) == 'LV':
                if jamo[1] in range(4520, 4547):
                    lv_part, t_part = jamo
                    t_index = t_part - T_BASE
                    return lv_part + t_index
                raise ValueError(fmt_str_invalid_sequence.format(jamo))
            else:
                pass
        raise ValueError(fmt_str_invalid_sequence.format(jamo))


def decompose_hangul_syllable(hangul_syllable, fully_decompose=False):
    """
    Function for taking a Unicode scalar value representing a Hangul syllable and decomposing it into a tuple
    representing the scalar values of the decomposed (canonical decomposition) Jamo.  If the Unicode scalar value
    passed in is not in the range of Hangul syllable values (as defined in UnicodeData.txt), a ValueError will be
    raised.

    The algorithm for doing the decomposition is described in the Unicode Standard, ch. 03, section 3.12,
    "Conjoining Jamo Behavior".

    Example: U+D4DB -> (U+D4CC, U+11B6)  # (canonical decomposition, default)
             U+D4DB -> (U+1111, U+1171, U+11B6)  # (full canonical decomposition)

    :param hangul_syllable: Unicode scalar value for Hangul syllable
    :param fully_decompose: Boolean indicating whether or not to do a canonical decomposition (default behavior is
                            fully_decompose=False) or a full canonical decomposition (fully_decompose=True)
    :return: Tuple of Unicode scalar values for the decomposed Jamo.
    """
    if not _is_hangul_syllable(hangul_syllable):
        raise ValueError('Value passed in does not represent a Hangul syllable!')
    s_index = hangul_syllable - S_BASE
    if fully_decompose:
        l_index = s_index // N_COUNT
        v_index = s_index % N_COUNT // T_COUNT
        t_index = s_index % T_COUNT
        l_part = L_BASE + l_index
        v_part = V_BASE + v_index
        t_part = T_BASE + t_index if t_index > 0 else None
        return (l_part, v_part, t_part)
    if _get_hangul_syllable_type(hangul_syllable) == 'LV':
        l_index = s_index // N_COUNT
        v_index = s_index % N_COUNT // T_COUNT
        l_part = L_BASE + l_index
        v_part = V_BASE + v_index
        return (l_part, v_part)
    lv_index = s_index // T_COUNT * T_COUNT
    t_index = s_index % T_COUNT
    lv_part = S_BASE + lv_index
    t_part = T_BASE + t_index
    return (lv_part, t_part)


def _get_hangul_syllable_name(hangul_syllable):
    """
    Function for taking a Unicode scalar value representing a Hangul syllable and converting it to its syllable name as
    defined by the Unicode naming rule NR1.  See the Unicode Standard, ch. 04, section 4.8, Names, for more information.

    :param hangul_syllable: Unicode scalar value representing the Hangul syllable to convert
    :return: String representing its syllable name as transformed according to naming rule NR1.
    """
    if not _is_hangul_syllable(hangul_syllable):
        raise ValueError('Value passed in does not represent a Hangul syllable!')
    jamo = decompose_hangul_syllable(hangul_syllable, fully_decompose=True)
    result = ''
    for j in jamo:
        if j is not None:
            result += _get_jamo_short_name(j)
        return result