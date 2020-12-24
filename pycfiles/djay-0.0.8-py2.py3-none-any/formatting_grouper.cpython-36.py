# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/formatting_grouper.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3326 bytes
from .utils import FlexibleIterator, BaronError

class UnExpectedSpaceToken(BaronError):
    pass


PRIORITY_ORDER = ('IMPORT', 'ENDL')
BOTH = ('SEMICOLON', 'AS', 'IMPORT', 'DOUBLE_STAR', 'DOT', 'LEFT_SQUARE_BRACKET', 'LEFT_PARENTHESIS',
        'STAR', 'SLASH', 'PERCENT', 'DOUBLE_SLASH', 'PLUS', 'MINUS', 'AT', 'LEFT_SHIFT',
        'RIGHT_SHIFT', 'AMPER', 'CIRCUMFLEX', 'VBAR', 'LESS', 'GREATER', 'EQUAL_EQUAL',
        'LESS_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'IN', 'IS', 'NOT', 'AND', 'OR',
        'IF', 'ELSE', 'EQUAL', 'PLUS_EQUAL', 'MINUS_EQUAL', 'STAR_EQUAL', 'AT_EQUAL',
        'SLASH_EQUAL', 'PERCENT_EQUAL', 'AMPER_EQUAL', 'VBAR_EQUAL', 'CIRCUMFLEX_EQUAL',
        'LEFT_SHIFT_EQUAL', 'RIGHT_SHIFT_EQUAL', 'DOUBLE_STAR_EQUAL', 'DOUBLE_SLASH_EQUAL',
        'ENDL', 'COMMA', 'FOR', 'COLON', 'BACKQUOTE', 'RIGHT_ARROW', 'FROM')
STRING = ('STRING', 'RAW_STRING', 'INTERPOLATED_STRING', 'INTERPOLATED_RAW_STRING',
          'UNICODE_STRING', 'UNICODE_RAW_STRING', 'BINARY_STRING', 'BINARY_RAW_STRING')
GROUP_SPACE_BEFORE = BOTH + ('RIGHT_PARENTHESIS', 'COMMENT') + STRING
GROUP_SPACE_AFTER = BOTH + ('TILDE', 'RETURN', 'YIELD', 'WITH', 'DEL', 'ASSERT', 'RAISE',
                            'EXEC', 'GLOBAL', 'NONLOCAL', 'PRINT', 'INDENT', 'WHILE',
                            'ELIF', 'EXCEPT', 'DEF', 'CLASS', 'LAMBDA')

def less_prioritary_than(a, b):
    if b not in PRIORITY_ORDER:
        return False
    else:
        if a not in PRIORITY_ORDER:
            return True
        return PRIORITY_ORDER.index(a) < PRIORITY_ORDER.index(b)


def group(sequence):
    return list(group_generator(sequence))


def group_generator(sequence):
    iterator = FlexibleIterator(sequence)
    while not iterator.end():
        current = next(iterator)
        if current is None:
            return
        if current[0] == 'SPACE':
            if iterator.show_next():
                if iterator.show_next()[0] in GROUP_SPACE_BEFORE:
                    new_current = next(iterator)
                    current = (new_current[0], new_current[1], [current])
        if current[0] in GROUP_SPACE_AFTER + STRING and iterator.show_next() and iterator.show_next()[0] == 'SPACE' and (not iterator.show_next(2) or iterator.show_next(2) and not less_prioritary_than(current[0], iterator.show_next(2)[0])):
            if current[0] in STRING:
                if iterator.show_next(2):
                    if iterator.show_next(2)[0] in GROUP_SPACE_BEFORE:
                        yield current
                        continue
            after_space = next(iterator)
            current = (current[0], current[1], current[2] if len(current) > 2 else [], [after_space])
        if current[0] == 'COLON':
            if iterator.show_next():
                if iterator.show_next()[0] == 'COMMENT':
                    comment = next(iterator)
                    current = (current[0], current[1], current[2] if len(current) > 2 else [], (current[3] if len(current) > 3 else []) + [comment])
        yield current