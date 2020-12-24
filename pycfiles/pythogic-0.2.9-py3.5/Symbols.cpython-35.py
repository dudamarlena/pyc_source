# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/base/Symbols.py
# Compiled at: 2018-03-06 10:46:37
# Size of source mod 2**32: 779 bytes
from enum import Enum

class Symbols(Enum):
    DUMMY_PROPOSITION = 'dummy_proposition'
    NOT = '~'
    AND = '&'
    OR = '|'
    EXISTS = '∃'
    FORALL = 'Ɐ'
    EQUAL = '='
    IMPLIES = '>>'
    EQUIVALENCE = '==='
    NEXT = '○'
    UNTIL = 'U'
    EVENTUALLY = '◇'
    ALWAYS = '□'
    PATH_UNION = '+'
    PATH_SEQUENCE = ';'
    PATH_STAR = '*'
    PATH_TEST = '?'
    ROUND_BRACKET_LEFT = '('
    ROUND_BRACKET_RIGHT = ')'
    ANGLE_BRACKET_LEFT = '❬'
    ANGLE_BRACKET_RIGHT = '❭'
    FULLWIDTH_SQUARE_BRACKET_LEFT = '［'
    FULLWIDTH_SQUARE_BRACKET_RIGHT = '］'
    TOP = '⊤'
    BOTTOM = '⊥'
    LAST = 'Last'
    END = 'End'
    LOGICAL_TRUE = '⊤⊤'
    LOGICAL_FALSE = '⊥⊥'
    CARET = '^'


ALL_SYMBOLS = {v.value for v in Symbols}