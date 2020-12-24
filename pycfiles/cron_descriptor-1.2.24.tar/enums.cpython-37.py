# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/chardet/chardet/enums.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 1661 bytes
__doc__ = '\nAll of the Enums that are used throughout the chardet package.\n\n:author: Dan Blanchard (dan.blanchard@gmail.com)\n'

class InputState(object):
    """InputState"""
    PURE_ASCII = 0
    ESC_ASCII = 1
    HIGH_BYTE = 2


class LanguageFilter(object):
    """LanguageFilter"""
    CHINESE_SIMPLIFIED = 1
    CHINESE_TRADITIONAL = 2
    JAPANESE = 4
    KOREAN = 8
    NON_CJK = 16
    ALL = 31
    CHINESE = CHINESE_SIMPLIFIED | CHINESE_TRADITIONAL
    CJK = CHINESE | JAPANESE | KOREAN


class ProbingState(object):
    """ProbingState"""
    DETECTING = 0
    FOUND_IT = 1
    NOT_ME = 2


class MachineState(object):
    """MachineState"""
    START = 0
    ERROR = 1
    ITS_ME = 2


class SequenceLikelihood(object):
    """SequenceLikelihood"""
    NEGATIVE = 0
    UNLIKELY = 1
    LIKELY = 2
    POSITIVE = 3

    @classmethod
    def get_num_categories(cls):
        """:returns: The number of likelihood categories in the enum."""
        return 4


class CharacterCategory(object):
    """CharacterCategory"""
    UNDEFINED = 255
    LINE_BREAK = 254
    SYMBOL = 253
    DIGIT = 252
    CONTROL = 251