# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/tryexcept.py
# Compiled at: 2020-02-08 15:24:06


def tryexcept(self, lhs, n, rule, ast, tokens, first, last):
    come_from_except = ast[(-1)]
    if rule == ('try_except', ('SETUP_EXCEPT', 'suite_stmts_opt', 'POP_BLOCK', 'except_handler', 'opt_come_from_except')):
        if come_from_except[0] == 'COME_FROM':
            return True
    elif rule == ('try_except', ('SETUP_EXCEPT', 'suite_stmts_opt', 'POP_BLOCK', 'except_handler', '\\e_opt_come_from_except')):
        for i in range(last, first, -1):
            if tokens[i] == 'END_FINALLY':
                jump_before_finally = tokens[(i - 1)]
                if jump_before_finally.kind.startswith('JUMP'):
                    if jump_before_finally == 'JUMP_FORWARD':
                        return tokens[(i - 1)].attr > tokens[last].off2int(prefer_last=True)
                    elif jump_before_finally == 'JUMP_BACK':
                        except_handler = ast[3]
                        if except_handler == 'except_handler' and except_handler[0] == 'JUMP_FORWARD':
                            return True
                        return False

        return False