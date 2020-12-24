# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/and_check.py
# Compiled at: 2020-02-16 17:43:52


def and_check(self, lhs, n, rule, ast, tokens, first, last):
    jmp = ast[1]
    if jmp.kind.startswith('jmp_'):
        if last == n:
            return True
        jmp_target = jmp[0].attr
        jmp_offset = jmp[0].offset
        if tokens[first].off2int() <= jmp_target < tokens[last].off2int():
            return True
        if rule == ('and', ('expr', 'jmp_false', 'expr', 'jmp_false')):
            jmp2_target = ast[3][0].attr
            return jmp_target != jmp2_target
        elif rule == ('and', ('expr', 'jmp_false', 'expr', 'POP_JUMP_IF_TRUE')):
            jmp2_target = ast[3].attr
            return jmp_target == jmp2_target
        elif rule == ('and', ('expr', 'jmp_false', 'expr')):
            if tokens[last] == 'POP_JUMP_IF_FALSE':
                return jmp_target != tokens[last].attr
            elif tokens[last] in ('POP_JUMP_IF_TRUE', 'JUMP_IF_TRUE_OR_POP'):
                if last + 1 < n and tokens[(last + 1)] == 'COME_FROM':
                    return jmp_target != tokens[(last + 1)].off2int()
                return jmp_target + 2 != tokens[last].attr
        elif rule == ('and', ('expr', 'jmp_false', 'expr', 'COME_FROM')):
            return ast[(-1)].attr != jmp_offset
        return jmp_target != tokens[last].off2int()
    return False