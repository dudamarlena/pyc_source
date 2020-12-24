# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/ifstmts_jump.py
# Compiled at: 2020-02-16 17:43:52
from uncompyle6.scanners.tok import Token

def ifstmts_jump(self, lhs, n, rule, ast, tokens, first, last):
    if len(rule[1]) <= 1 or not ast:
        return False
    come_froms = ast[(-1)]
    pop_jump_index = first - 1
    while pop_jump_index > 0 and tokens[pop_jump_index] in ('ELSE', 'POP_TOP', 'JUMP_FORWARD',
                                                            'COME_FROM'):
        pop_jump_index -= 1

    if tokens[pop_jump_index].attr > 256:
        return False
    pop_jump_offset = tokens[pop_jump_index].off2int(prefer_last=False)
    if isinstance(come_froms, Token):
        if tokens[pop_jump_index].attr < pop_jump_offset and ast[0] != 'pass':
            return False
        return come_froms.attr is not None and pop_jump_offset > come_froms.attr
    elif len(come_froms) == 0:
        return False
    else:
        return pop_jump_offset > come_froms[(-1)].attr
    return