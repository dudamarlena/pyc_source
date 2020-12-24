# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/ifstmt.py
# Compiled at: 2020-02-16 17:43:52


def ifstmt(self, lhs, n, rule, ast, tokens, first, last):
    if lhs == 'ifstmtl':
        if last == n:
            last -= 1
        if tokens[last].attr and isinstance(tokens[last].attr, int):
            if tokens[first].offset >= tokens[last].attr:
                return True
    l = last
    if l == n:
        l -= 1
    if isinstance(tokens[l].offset, str):
        last_offset = int(tokens[l].offset.split('_')[0], 10)
    else:
        last_offset = tokens[l].offset
    for i in range(first, l):
        t = tokens[i]
        if t.kind in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE'):
            pjif_target = t.attr
            target_instr = self.insts[self.offset2inst_index[pjif_target]]
            if lhs == 'iflaststmtl' and target_instr.opname == 'JUMP_ABSOLUTE':
                pjif_target = target_instr.arg
            if pjif_target > last_offset:
                if tokens[l] == 'JUMP_FORWARD':
                    return tokens[l].attr != pjif_target
                return True
            elif lhs == 'ifstmtl' and tokens[first].off2int() > pjif_target:
                return False

    if ast:
        testexpr = ast[0]
        if last + 1 < n and tokens[(last + 1)] == 'COME_FROM_LOOP':
            return True
        if testexpr[0] in ('testtrue', 'testfalse'):
            test = testexpr[0]
            if len(test) > 1 and test[1].kind.startswith('jmp_'):
                jmp_target = test[1][0].attr
                if tokens[first].off2int(prefer_last=True) <= jmp_target < tokens[last].off2int(prefer_last=False):
                    return True
                if jmp_target > tokens[last].off2int():
                    if jmp_target == tokens[(last - 1)].attr:
                        return False
                    if last < n and tokens[last].kind.startswith('JUMP'):
                        return False
                    return True
    return False