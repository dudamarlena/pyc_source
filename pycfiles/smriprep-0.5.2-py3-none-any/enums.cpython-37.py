# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_vendor/chardet/enums.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 1661 bytes
"""
All of the Enums that are used throughout the chardet package.

:author: Dan Blanchard (dan.blanchard@gmail.com)
"""

class InputState(object):
    __doc__ = '\n    This enum represents the different states a universal detector can be in.\n    '
    PURE_ASCII = 0
    ESC_ASCII = 1
    HIGH_BYTE = 2


class LanguageFilter(object):
    __doc__ = '\n    This enum represents the different language filters we can apply to a\n    ``UniversalDetector``.\n    '
    CHINESE_SIMPLIFIED = 1
    CHINESE_TRADITIONAL = 2
    JAPANESE = 4
    KOREAN = 8
    NON_CJK = 16
    ALL = 31
    CHINESE = CHINESE_SIMPLIFIED | CHINESE_TRADITIONAL
    CJK = CHINESE | JAPANESE | KOREAN


class ProbingState(object):
    __doc__ = '\n    This enum represents the different states a prober can be in.\n    '
    DETECTING = 0
    FOUND_IT = 1
    NOT_ME = 2


class MachineState(object):
    __doc__ = '\n    This enum represents the different states a state machine can be in.\n    '
    START = 0
    ERROR = 1
    ITS_ME = 2


class SequenceLikelihood(object):
    __doc__ = '\n    This enum represents the likelihood of a character following the previous one.\n    '
    NEGATIVE = 0
    UNLIKELY = 1
    LIKELY = 2
    POSITIVE = 3

    @classmethod
    def get_num_categories(cls):
        """:returns: The number of likelihood categories in the enum."""
        return 4


class CharacterCategory(object):
    __doc__ = '\n    This enum represents the different categories language models for\n    ``SingleByteCharsetProber`` put characters into.\n\n    Anything less than CONTROL is considered a letter.\n    '
    UNDEFINED = 255
    LINE_BREAK = 254
    SYMBOL = 253
    DIGIT = 252
    CONTROL = 251