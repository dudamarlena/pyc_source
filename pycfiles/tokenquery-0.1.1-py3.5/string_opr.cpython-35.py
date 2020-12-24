# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/acceptors/core/string_opr.py
# Compiled at: 2017-01-28 16:40:48
# Size of source mod 2**32: 1833 bytes
import re

def str_eq(token_input, operation_input):
    if token_input == operation_input:
        return True
    return False


def str_reg(token_input, operation_input):
    if not token_input:
        return False
    else:
        if re.match(operation_input, token_input):
            return True
        return False


def str_len(token_input, operation_input):
    cond_type = ''
    comp_part = operation_input.lstrip().strip()[:2]
    if comp_part in ('==', '>=', '<=', '!=', '<>'):
        cond_type = comp_part
        try:
            cond_value = int(operation_input.lstrip().strip()[2:])
        except ValueError:
            return False

    elif comp_part[0] in ('=', '>', '<'):
        cond_type = comp_part[0]
        try:
            cond_value = int(operation_input.lstrip().strip()[1:])
        except ValueError:
            return False

    else:
        return 'unknown operation'
    try:
        text_len = len(token_input)
        if cond_type == '==' or cond_type == '=':
            return text_len == cond_value
        else:
            if cond_type == '<':
                return text_len < cond_value
            if cond_type == '>':
                return text_len > cond_value
            if cond_type == '>=':
                return text_len >= cond_value
            if cond_type == '<=':
                return text_len <= cond_value
            if cond_type == '!=' or cond_type == '<>':
                return text_len != cond_value
            return False
    except ValueError:
        return False