# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/except_handler_else.py
# Compiled at: 2020-02-08 15:24:06


def except_handler_else(self, lhs, n, rule, ast, tokens, first, last):
    if self.version not in (2.7, 3.5):
        return False
    if tokens[first] in ('JUMP_FORWARD', 'JUMP_ABSOLUTE'):
        first_jump_target = tokens[first].pattr
        last = min(last, len(tokens) - 1)
        for i in range(last, first, -1):
            if tokens[i] == 'END_FINALLY':
                i -= 1
                second_jump = tokens[i]
                if second_jump in ('JUMP_FORWARD', 'JUMP_ABSOLUTE'):
                    second_jump_target = second_jump.pattr
                    equal_target = second_jump_target == first_jump_target
                    if equal_target:
                        return lhs != 'except_handler'
                    else:
                        return lhs != 'except_handler_else'
                else:
                    return False

    return False