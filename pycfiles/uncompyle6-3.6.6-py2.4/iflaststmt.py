# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/iflaststmt.py
# Compiled at: 2020-02-08 15:24:06


def iflaststmt(self, lhs, n, rule, ast, tokens, first, last):
    testexpr = ast[0]
    if testexpr[0] in ('testtrue', 'testfalse'):
        test = testexpr[0]
        if len(test) > 1 and test[1].kind.startswith('jmp_'):
            if last == n:
                last -= 1
            jmp_target = test[1][0].attr
            if tokens[first].off2int() <= jmp_target < tokens[last].off2int():
                return True
            if last + 1 < n and tokens[(last - 1)] != 'JUMP_BACK' and tokens[(last + 1)] == 'COME_FROM_LOOP':
                return True
            if first > 0 and tokens[(first - 1)] == 'POP_JUMP_IF_FALSE':
                return tokens[(first - 1)].attr == jmp_target
            if jmp_target > tokens[last].off2int():
                if jmp_target == tokens[(last - 1)].attr:
                    return False
                if last < n and tokens[last].kind.startswith('JUMP'):
                    return False
                return True
    return False