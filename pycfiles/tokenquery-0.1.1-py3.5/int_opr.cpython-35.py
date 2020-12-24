# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/acceptors/core/int_opr.py
# Compiled at: 2017-01-28 16:40:22
# Size of source mod 2**32: 2852 bytes


def int_value(token_input, operation_input):
    cond_type = ''
    comp_part = operation_input.lstrip().strip()[:2]
    if comp_part in ('==', '>=', '<=', '!=', '<>'):
        cond_type = comp_part
        try:
            cond_value = int(operation_input.lstrip().strip()[2:])
        except ValueError:
            return False

    if comp_part[0] in ('=', '>', '<'):
        cond_type = comp_part[0]
        try:
            cond_value = int(operation_input.lstrip().strip()[1:])
        except ValueError:
            return False

    try:
        text_value = int(token_input)
        if cond_type == '=' or cond_type == '==':
            return text_value == cond_value
        else:
            if cond_type == '<':
                return text_value < cond_value
            if cond_type == '>':
                return text_value > cond_value
            if cond_type == '>=':
                return text_value >= cond_value
            if cond_type == '<=':
                return text_value <= cond_value
            if cond_type == '!=' or cond_type == '<>':
                return text_value != cond_value
            return False
    except ValueError:
        return False


def int_e(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value == op_value
    except ValueError:
        return False


def int_g(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value > op_value
    except ValueError:
        return False


def int_l(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value < op_value
    except ValueError:
        return False


def int_ne(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value != op_value
    except ValueError:
        return False


def int_le(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value <= op_value
    except ValueError:
        return False


def int_ge(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value >= op_value
    except ValueError:
        return False