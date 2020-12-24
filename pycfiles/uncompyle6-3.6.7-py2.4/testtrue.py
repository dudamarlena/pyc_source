# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/testtrue.py
# Compiled at: 2020-02-08 15:24:06


def testtrue(self, lhs, n, rule, ast, tokens, first, last):
    if self.version != 3.7:
        return False
    if rule == ('testtrue', ('expr', 'jmp_true')):
        pjit = tokens[min(last - 1, n - 2)]
        if pjit == 'POP_JUMP_IF_TRUE' and tokens[first].off2int() > pjit.attr:
            assert_next = tokens[min(last + 1, n - 1)]
            return assert_next != 'RAISE_VARARGS_1'
    elif rule == ('testfalsel', ('expr', 'jmp_true')):
        pjit = tokens[min(last - 1, n - 2)]
        if pjit == 'POP_JUMP_IF_TRUE' and tokens[first].off2int() > pjit.attr:
            assert_next = tokens[min(last + 1, n - 1)]
            return assert_next == 'RAISE_VARARGS_1'
    return False