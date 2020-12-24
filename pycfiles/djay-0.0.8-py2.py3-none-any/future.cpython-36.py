# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/future.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 1067 bytes


def has_print_function(tokens):
    p = 0
    while p < len(tokens):
        if tokens[p][0] != 'FROM':
            p += 1
        elif tokens[(p + 1)][0:2] != ('NAME', '__future__'):
            p += 1
        elif tokens[(p + 2)][0] != 'IMPORT':
            p += 1
        else:
            current = p + 3
            if tokens[current][0] == 'LEFT_PARENTHESIS':
                current += 1
            while current < len(tokens) and tokens[current][0] == 'NAME':
                if tokens[current][1] == 'print_function':
                    return True
                if current + 1 < len(tokens) and tokens[(current + 1)][0] == 'AS':
                    current += 4
                else:
                    current += 2

            p += 1

    return False


def replace_print_by_name(tokens):

    def is_print(token):
        return token[0] == 'PRINT'

    return [('NAME', 'print') if is_print(x) else x for x in tokens]