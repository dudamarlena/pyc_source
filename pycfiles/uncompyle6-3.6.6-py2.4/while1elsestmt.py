# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/while1elsestmt.py
# Compiled at: 2020-02-08 15:24:06


def while1elsestmt(self, lhs, n, rule, ast, tokens, first, last):
    if last == n:
        last -= 1
    if tokens[last] == 'COME_FROM_LOOP':
        last -= 1
    elif tokens[(last - 1)] == 'COME_FROM_LOOP':
        last -= 2
    if tokens[last] in ('JUMP_BACK', 'CONTINUE'):
        return True
    last += 1
    return self.version < 3.8 and tokens[first].attr > tokens[last].off2int()