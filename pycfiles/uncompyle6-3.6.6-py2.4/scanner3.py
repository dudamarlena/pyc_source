# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner3.py
# Compiled at: 2020-04-20 22:51:00
"""
Python 3 Generic bytecode scanner/deparser

This overlaps various Python3's dis module, but it can be run from
Python versions other than the version running this code. Notably,
run from Python version 2.

Also we *modify* the instruction sequence to assist deparsing code.
For example:
 -  we add "COME_FROM" instructions to help in figuring out
    conditional branching and looping.
 -  LOAD_CONSTs are classified further into the type of thing
    they load:
      lambda's, genexpr's, {dict,set,list} comprehension's,
 -  PARAMETER counts appended  {CALL,MAKE}_FUNCTION, BUILD_{TUPLE,SET,SLICE}

Finally we save token information.
"""
from uncompyle6 import PYTHON_VERSION
if PYTHON_VERSION < 2.6:
    from xdis.namedtuple24 import namedtuple
else:
    from collections import namedtuple
from xdis import iscode
from xdis.bytecode import instruction_size, _get_const_info
from uncompyle6.scanner import Token, parse_fn_counts
import xdis, xdis.opcodes.opcode_33 as op3
from uncompyle6.scanner import Scanner
import sys
from uncompyle6 import PYTHON3
if PYTHON3:
    intern = sys.intern
globals().update(op3.opmap)

class Scanner3(Scanner):
    __module__ = __name__

    def __init__(self, version, show_asm=None, is_pypy=False):
        super(Scanner3, self).__init__(version, show_asm, is_pypy)
        if self.version < 3.8:
            setup_ops = [
             self.opc.SETUP_LOOP, self.opc.SETUP_EXCEPT, self.opc.SETUP_FINALLY]
            self.setup_ops_no_loop = frozenset(setup_ops) - frozenset([self.opc.SETUP_LOOP])
        else:
            setup_ops = [self.opc.SETUP_FINALLY]
            self.setup_ops_no_loop = frozenset(setup_ops)
        if self.version >= 3.2:
            setup_ops.append(self.opc.SETUP_WITH)
        self.setup_ops = frozenset(setup_ops)
        if self.version == 3.0:
            self.pop_jump_tf = frozenset([self.opc.JUMP_IF_FALSE, self.opc.JUMP_IF_TRUE])
            self.not_continue_follow = ('END_FINALLY', 'POP_BLOCK', 'POP_TOP')
        else:
            self.pop_jump_tf = frozenset([self.opc.PJIF, self.opc.PJIT])
            self.not_continue_follow = ('END_FINALLY', 'POP_BLOCK')
        statement_opcodes = [
         self.opc.POP_BLOCK, self.opc.STORE_FAST, self.opc.DELETE_FAST, self.opc.STORE_DEREF, self.opc.STORE_GLOBAL, self.opc.DELETE_GLOBAL, self.opc.STORE_NAME, self.opc.DELETE_NAME, self.opc.STORE_ATTR, self.opc.DELETE_ATTR, self.opc.STORE_SUBSCR, self.opc.POP_TOP, self.opc.DELETE_SUBSCR, self.opc.END_FINALLY, self.opc.RETURN_VALUE, self.opc.RAISE_VARARGS, self.opc.PRINT_EXPR, self.opc.JUMP_ABSOLUTE]
        if self.version < 3.8:
            statement_opcodes += [self.opc.BREAK_LOOP, self.opc.CONTINUE_LOOP]
        self.statement_opcodes = frozenset(statement_opcodes) | self.setup_ops_no_loop
        self.designator_ops = frozenset([self.opc.STORE_FAST, self.opc.STORE_NAME, self.opc.STORE_GLOBAL, self.opc.STORE_DEREF, self.opc.STORE_ATTR, self.opc.STORE_SUBSCR, self.opc.UNPACK_SEQUENCE, self.opc.JUMP_ABSOLUTE, self.opc.UNPACK_EX])
        if self.version > 3.0:
            self.jump_if_pop = frozenset([self.opc.JUMP_IF_FALSE_OR_POP, self.opc.JUMP_IF_TRUE_OR_POP])
            self.pop_jump_if_pop = frozenset([self.opc.JUMP_IF_FALSE_OR_POP, self.opc.JUMP_IF_TRUE_OR_POP, self.opc.POP_JUMP_IF_TRUE, self.opc.POP_JUMP_IF_FALSE])
            self.statement_opcode_sequences = [
             (
              self.opc.POP_JUMP_IF_FALSE, self.opc.JUMP_FORWARD), (self.opc.POP_JUMP_IF_FALSE, self.opc.JUMP_ABSOLUTE), (self.opc.POP_JUMP_IF_TRUE, self.opc.JUMP_FORWARD), (self.opc.POP_JUMP_IF_TRUE, self.opc.JUMP_ABSOLUTE)]
        else:
            self.jump_if_pop = frozenset([])
            self.pop_jump_if_pop = frozenset([])
            self.statement_opcode_sequences = [
             (
              self.opc.JUMP_FORWARD,), (self.opc.JUMP_ABSOLUTE,), (self.opc.JUMP_FORWARD,), (self.opc.JUMP_ABSOLUTE,)]
        varargs_ops = set([self.opc.BUILD_LIST, self.opc.BUILD_TUPLE, self.opc.BUILD_SET, self.opc.BUILD_SLICE, self.opc.BUILD_MAP, self.opc.UNPACK_SEQUENCE, self.opc.RAISE_VARARGS])
        if is_pypy or self.version >= 3.7:
            varargs_ops.add(self.opc.CALL_METHOD)
        if self.version >= 3.5:
            varargs_ops |= set([self.opc.BUILD_SET_UNPACK, self.opc.BUILD_MAP_UNPACK, self.opc.BUILD_LIST_UNPACK, self.opc.BUILD_TUPLE_UNPACK])
            if self.version >= 3.6:
                varargs_ops.add(self.opc.BUILD_CONST_KEY_MAP)
                self.MAKE_FUNCTION_FLAGS = tuple(('\n                 default keyword-only annotation closure').split())
        self.varargs_ops = frozenset(varargs_ops)

    def ingest(self, co, classname=None, code_objects={}, show_asm=None):
        """
        Pick out tokens from an uncompyle6 code object, and transform them,
        returning a list of uncompyle6 Token's.

        The transformations are made to assist the deparsing grammar.
        Specificially:
           -  various types of LOAD_CONST's are categorized in terms of what they load
           -  COME_FROM instructions are added to assist parsing control structures
           -  MAKE_FUNCTION and FUNCTION_CALLS append the number of positional arguments
           -  some EXTENDED_ARGS instructions are removed

        Also, when we encounter certain tokens, we add them to a set which will cause custom
        grammar rules. Specifically, variable arg tokens like MAKE_FUNCTION or BUILD_LIST
        cause specific rules for the specific number of arguments they take.
        """
        if not show_asm:
            show_asm = self.show_asm
        if not show_asm:
            show_asm = self.show_asm
        bytecode = self.build_instructions(co)
        if show_asm in ('both', 'before'):
            for instr in bytecode.get_instructions(co):
                print instr.disassemble()

        tokens = []
        customize = {}
        if self.is_pypy:
            customize['PyPy'] = 0
        self.load_asserts = set()
        n = len(self.insts)
        for (i, inst) in enumerate(self.insts):
            if self.version == 3.0:
                assert_can_follow = inst.opname == 'POP_TOP' and i + 1 < n
                if assert_can_follow:
                    prev_inst = self.insts[(i - 1)]
                    assert_can_follow = prev_inst.opname in ('JUMP_IF_TRUE', 'JUMP_IF_FALSE') and i + 1 < n
                    jump_if_inst = prev_inst
            else:
                assert_can_follow = inst.opname in ('POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE') and i + 1 < n
                jump_if_inst = inst
            if assert_can_follow:
                next_inst = self.insts[(i + 1)]
                if next_inst.opname == 'LOAD_GLOBAL' and next_inst.argval == 'AssertionError' and jump_if_inst.argval:
                    raise_idx = self.offset2inst_index[self.prev_op[jump_if_inst.argval]]
                    raise_inst = self.insts[raise_idx]
                    if raise_inst.opname.startswith('RAISE_VARARGS'):
                        self.load_asserts.add(next_inst.offset)

        jump_targets = self.find_jump_targets(show_asm)
        last_op_was_break = False
        for (i, inst) in enumerate(self.insts):
            argval = inst.argval
            op = inst.opcode
            if inst.opname == 'EXTENDED_ARG':
                if i + 1 < n:
                    if self.insts[(i + 1)].opcode != self.opc.MAKE_FUNCTION:
                        continue
                if inst.offset in jump_targets:
                    jump_idx = 0
                    for jump_offset in sorted(jump_targets[inst.offset], reverse=True):
                        come_from_name = 'COME_FROM'
                        opname = self.opname_for_offset(jump_offset)
                        if opname == 'EXTENDED_ARG':
                            j = xdis.next_offset(op, self.opc, jump_offset)
                            opname = self.opname_for_offset(j)
                        if opname.startswith('SETUP_'):
                            come_from_type = opname[len('SETUP_'):]
                            come_from_name = 'COME_FROM_%s' % come_from_type
                        elif inst.offset in self.except_targets:
                            come_from_name = 'COME_FROM_EXCEPT_CLAUSE'
                        tokens.append(Token(come_from_name, jump_offset, repr(jump_offset), offset='%s_%s' % (inst.offset, jump_idx), has_arg=True, opc=self.opc))
                        jump_idx += 1

                if inst.offset in self.else_start:
                    end_offset = self.else_start[inst.offset]
                    tokens.append(Token('ELSE', None, repr(end_offset), offset='%s' % inst.offset, has_arg=True, opc=self.opc))
                pattr = inst.argrepr
                opname = inst.opname
                if op in self.opc.CONST_OPS:
                    const = argval
                    if iscode(const):
                        assert const.co_name == '<lambda>' and opname == 'LOAD_CONST'
                        opname = 'LOAD_LAMBDA'
                    elif const.co_name == '<genexpr>':
                        opname = 'LOAD_GENEXPR'
                    elif const.co_name == '<dictcomp>':
                        opname = 'LOAD_DICTCOMP'
                    elif const.co_name == '<setcomp>':
                        opname = 'LOAD_SETCOMP'
                    elif const.co_name == '<listcomp>':
                        opname = 'LOAD_LISTCOMP'
                    else:
                        opname = 'LOAD_CODE'
                    pattr = '<code_object ' + const.co_name + '>'
                elif isinstance(const, str) or xdis.PYTHON_VERSION <= 2.7 and isinstance(const, unicode):
                    opname = 'LOAD_STR'
                else:
                    if isinstance(inst.arg, int) and inst.arg < len(co.co_consts):
                        (argval, _) = _get_const_info(inst.arg, co.co_consts)
                    pattr = const
            elif opname in ('MAKE_FUNCTION', 'MAKE_CLOSURE'):
                if self.version >= 3.6:
                    flags = argval
                    opname = 'MAKE_FUNCTION_%d' % flags
                    attr = []
                    for flag in self.MAKE_FUNCTION_FLAGS:
                        bit = flags & 1
                        attr.append(bit)
                        flags >>= 1

                    attr = attr[:4]
                else:
                    (pos_args, name_pair_args, annotate_args) = parse_fn_counts(inst.argval)
                    pattr = '%d positional, %d keyword only, %d annotated' % (pos_args, name_pair_args, annotate_args)
                    if name_pair_args > 0:
                        opname = '%s_N%d' % (opname, name_pair_args)
                    if annotate_args > 0:
                        opname = '%s_A_%d' % (opname, annotate_args)
                    opname = '%s_%d' % (opname, pos_args)
                    attr = (pos_args, name_pair_args, annotate_args)
                tokens.append(Token(opname=opname, attr=attr, pattr=pattr, offset=inst.offset, linestart=inst.starts_line, op=op, has_arg=inst.has_arg, opc=self.opc))
                continue
            elif op in self.varargs_ops:
                pos_args = argval
                if self.is_pypy and not pos_args and opname == 'BUILD_MAP':
                    opname = 'BUILD_MAP_n'
                else:
                    opname = '%s_%d' % (opname, pos_args)
            elif self.is_pypy and opname in ('JUMP_IF_NOT_DEBUG', 'CALL_FUNCTION'):
                if opname == 'JUMP_IF_NOT_DEBUG':
                    customize[opname] = 0
                elif self.version >= 3.6 and argval > 255:
                    opname = 'CALL_FUNCTION_KW'
            elif opname == 'UNPACK_EX':
                before_args = argval & 255
                after_args = argval >> 8 & 255
                pattr = '%d before vararg, %d after' % (before_args, after_args)
                argval = (before_args, after_args)
                opname = '%s_%d+%d' % (opname, before_args, after_args)
            elif op == self.opc.JUMP_ABSOLUTE:
                pattr = argval
                target = self.get_target(inst.offset)
                if target <= inst.offset:
                    next_opname = self.insts[(i + 1)].opname
                    is_continue = self.insts[self.offset2inst_index[target]].opname == 'FOR_ITER' and self.insts[(i + 1)].opname == 'JUMP_FORWARD'
                    if self.version == 3.0 and self.insts[(i + 1)].opname == 'JUMP_FORWARD' and not is_continue:
                        target_prev = self.offset2inst_index[self.prev_op[target]]
                        is_continue = self.insts[target_prev].opname == 'SETUP_LOOP'
                    if is_continue or inst.offset in self.stmts and inst.starts_line and next_opname not in self.not_continue_follow:
                        opname = 'CONTINUE'
                    else:
                        opname = 'JUMP_BACK'
                        if tokens[(-1)].kind == 'JUMP_BACK' and tokens[(-1)].attr <= argval:
                            if tokens[(-2)].kind == 'BREAK_LOOP':
                                del tokens[-1]
                            else:
                                tokens[(-1)].kind = intern('CONTINUE')
                    if last_op_was_break and opname == 'CONTINUE':
                        last_op_was_break = False
                        continue
            elif op == self.opc.RETURN_VALUE:
                if inst.offset in self.return_end_ifs:
                    opname = 'RETURN_END_IF'
            elif inst.offset in self.load_asserts:
                opname = 'LOAD_ASSERT'
            last_op_was_break = opname == 'BREAK_LOOP'
            tokens.append(Token(opname=opname, attr=argval, pattr=pattr, offset=inst.offset, linestart=inst.starts_line, op=op, has_arg=inst.has_arg, opc=self.opc))

        if show_asm in ('both', 'after'):
            for t in tokens:
                print t.format(line_prefix='')

            print ()
        return (
         tokens, customize)

    def find_jump_targets(self, debug):
        """
        Detect all offsets in a byte code which are jump targets
        where we might insert a COME_FROM instruction.

        Return the list of offsets.

        Return the list of offsets. An instruction can be jumped
        to in from multiple instructions.
        """
        code = self.code
        n = len(code)
        self.structs = [{'type': 'root', 'start': 0, 'end': n - 1}]
        self.loops = []
        self.fixed_jumps = {}
        self.except_targets = {}
        self.ignore_if = set()
        self.build_statement_indices()
        self.else_start = {}
        self.not_continue = set()
        self.return_end_ifs = set()
        self.setup_loop_targets = {}
        self.setup_loops = {}
        targets = {}
        for (i, inst) in enumerate(self.insts):
            offset = inst.offset
            op = inst.opcode
            self.detect_control_flow(offset, targets, i)
            if inst.has_arg:
                label = self.fixed_jumps.get(offset)
                oparg = inst.arg
                if self.version >= 3.6 and self.code[offset] == self.opc.EXTENDED_ARG:
                    j = xdis.next_offset(op, self.opc, offset)
                    next_offset = xdis.next_offset(op, self.opc, j)
                else:
                    next_offset = xdis.next_offset(op, self.opc, offset)
                if label is None:
                    if op in self.opc.hasjrel and op != self.opc.FOR_ITER:
                        label = next_offset + oparg
                    elif op in self.opc.hasjabs:
                        if op in self.jump_if_pop:
                            if oparg > offset:
                                label = oparg
                if label is not None and label != -1:
                    targets[label] = targets.get(label, []) + [offset]
            elif op == self.opc.END_FINALLY and offset in self.fixed_jumps:
                label = self.fixed_jumps[offset]
                targets[label] = targets.get(label, []) + [offset]

        if debug in ('both', 'after'):
            import pprint as pp
            pp.pprint(self.structs)
        return targets

    def build_statement_indices(self):
        code = self.code
        start = 0
        end = codelen = len(code)
        prelim = self.inst_matches(start, end, self.statement_opcodes)
        stmts = self.stmts = set(prelim)
        pass_stmts = set()
        for sequence in self.statement_opcode_sequences:
            for i in self.op_range(start, end - (len(sequence) + 1)):
                match = True
                for elem in sequence:
                    if elem != code[i]:
                        match = False
                        break
                    i += instruction_size(code[i], self.opc)

                if match is True:
                    i = self.prev_op[i]
                    stmts.add(i)
                    pass_stmts.add(i)

        if pass_stmts:
            stmt_offset_list = list(stmts)
            stmt_offset_list.sort()
        else:
            stmt_offset_list = prelim
        self.next_stmt = slist = []
        last_stmt_offset = -1
        i = 0
        for stmt_offset in stmt_offset_list:
            if code[stmt_offset] == self.opc.JUMP_ABSOLUTE and stmt_offset not in pass_stmts:
                target = self.get_target(stmt_offset)
                if target > stmt_offset or self.lines[last_stmt_offset].l_no == self.lines[stmt_offset].l_no:
                    stmts.remove(stmt_offset)
                    continue
                j = self.prev_op[stmt_offset]
                while code[j] == self.opc.JUMP_ABSOLUTE:
                    j = self.prev_op[j]

                if code[j] == self.opc.LIST_APPEND:
                    stmts.remove(stmt_offset)
                    continue
            elif code[stmt_offset] == self.opc.POP_TOP and code[self.prev_op[stmt_offset]] == self.opc.ROT_TWO:
                stmts.remove(stmt_offset)
                continue
            elif code[stmt_offset] in self.designator_ops:
                j = self.prev_op[stmt_offset]
                while code[j] in self.designator_ops:
                    j = self.prev_op[j]

                if code[j] == self.opc.FOR_ITER:
                    stmts.remove(stmt_offset)
                    continue
            slist += [stmt_offset] * (stmt_offset - i)
            last_stmt_offset = stmt_offset
            i = stmt_offset

        slist += [codelen] * (codelen - len(slist))

    def detect_control_flow(self, offset, targets, inst_index):
        """
        Detect type of block structures and their boundaries to fix optimized jumps
        in python2.3+
        """
        code = self.code
        inst = self.insts[inst_index]
        op = inst.opcode
        parent = self.structs[0]
        start = parent['start']
        end = parent['end']
        for struct in self.structs:
            current_start = struct['start']
            current_end = struct['end']
            if current_start <= offset < current_end and current_start >= start and current_end <= end:
                start = current_start
                end = current_end
                parent = struct

        if self.version < 3.8:
            if op == self.opc.SETUP_LOOP:
                start += inst.inst_size
                target = self.get_target(offset)
                end = self.restrict_to_parent(target, parent)
                self.setup_loops[target] = offset
                if target != end:
                    self.fixed_jumps[offset] = end
                (line_no, next_line_byte) = self.lines[offset]
                jump_back = self.last_instr(start, end, self.opc.JUMP_ABSOLUTE, next_line_byte, False)
                if jump_back:
                    jump_forward_offset = xdis.next_offset(code[jump_back], self.opc, jump_back)
                else:
                    jump_forward_offset = None
                return_val_offset1 = self.prev[self.prev[end]]
                if jump_back and jump_back != self.prev_op[end] and self.is_jump_forward(jump_forward_offset):
                    if code[self.prev_op[end]] == self.opc.RETURN_VALUE or code[self.prev_op[end]] == self.opc.POP_BLOCK and code[return_val_offset1] == self.opc.RETURN_VALUE:
                        jump_back = None
                jump_back = jump_back or self.last_instr(start, end, self.opc.RETURN_VALUE)
                if not jump_back:
                    return
                jb_inst = self.get_inst(jump_back)
                jump_back = self.next_offset(jb_inst.opcode, jump_back)
                if_offset = None
                if code[self.prev_op[next_line_byte]] not in self.pop_jump_tf:
                    if_offset = self.prev[next_line_byte]
                if if_offset:
                    loop_type = 'while'
                    self.ignore_if.add(if_offset)
                else:
                    loop_type = 'for'
                target = next_line_byte
                end = xdis.next_offset(code[jump_back], self.opc, jump_back)
            else:
                if self.get_target(jump_back) >= next_line_byte:
                    jump_back = self.last_instr(start, end, self.opc.JUMP_ABSOLUTE, start, False)
                jb_inst = self.get_inst(jump_back)
                jb_next_offset = self.next_offset(jb_inst.opcode, jump_back)
                if end > jb_next_offset and self.is_jump_forward(end):
                    if self.is_jump_forward(jb_next_offset):
                        if self.get_target(jb_next_offset) == self.get_target(end):
                            self.fixed_jumps[offset] = jb_next_offset
                            end = jb_next_offset
                elif target < offset:
                    self.fixed_jumps[offset] = jb_next_offset
                    end = jb_next_offset
                target = self.get_target(jump_back)
                if code[target] in (self.opc.FOR_ITER, self.opc.GET_ITER):
                    loop_type = 'for'
                else:
                    loop_type = 'while'
                    test = self.prev_op[next_line_byte]
                    if test == offset:
                        loop_type = 'while 1'
                    elif self.code[test] in self.opc.JUMP_OPs:
                        self.ignore_if.add(test)
                        test_target = self.get_target(test)
                        if test_target > jump_back + 3:
                            jump_back = test_target
                self.not_continue.add(jump_back)
            self.loops.append(target)
            self.structs.append({'type': loop_type + '-loop', 'start': target, 'end': jump_back})
            after_jump_offset = xdis.next_offset(code[jump_back], self.opc, jump_back)
            if after_jump_offset != end:
                self.structs.append({'type': loop_type + '-else', 'start': after_jump_offset, 'end': end})
        elif op in self.pop_jump_tf:
            start = offset + inst.inst_size
            target = inst.argval
            rtarget = self.restrict_to_parent(target, parent)
            prev_op = self.prev_op
            if target != rtarget:
                if parent['type'] == 'and/or':
                    self.fixed_jumps[offset] = rtarget
                    return
                pretarget = self.get_inst(prev_op[target])
                if pretarget.opcode in self.pop_jump_if_pop and target > offset and pretarget.offset != offset:
                    if self.version < 3.5 or pretarget.argval != target:
                        self.fixed_jumps[offset] = pretarget.offset
                        self.structs.append({'type': 'and/or', 'start': start, 'end': pretarget.offset})
                        return
                pre_rtarget = prev_op[rtarget]
                if op == self.opc.POP_JUMP_IF_FALSE:
                    match = self.rem_or(start, self.next_stmt[offset], self.opc.POP_JUMP_IF_FALSE, target)
                    if match:
                        is_jump_forward = self.is_jump_forward(pre_rtarget)
                        if is_jump_forward and pre_rtarget not in self.stmts and self.restrict_to_parent(self.get_target(pre_rtarget), parent) == rtarget:
                            if code[prev_op[pre_rtarget]] == self.opc.JUMP_ABSOLUTE and self.remove_mid_line_ifs([offset]) and target == self.get_target(prev_op[pre_rtarget]) and (prev_op[pre_rtarget] not in self.stmts or self.get_target(prev_op[pre_rtarget]) > prev_op[pre_rtarget]) and 1 == len(self.remove_mid_line_ifs(self.rem_or(start, prev_op[pre_rtarget], self.pop_jump_tf, target))):
                                pass
                            elif code[prev_op[pre_rtarget]] == self.opc.RETURN_VALUE and self.remove_mid_line_ifs([offset]) and 1 == len(set(self.remove_mid_line_ifs(self.rem_or(start, prev_op[pre_rtarget], self.pop_jump_tf, target))) | set(self.remove_mid_line_ifs(self.rem_or(start, prev_op[pre_rtarget], (
                             self.opc.POP_JUMP_IF_FALSE, self.opc.POP_JUMP_IF_TRUE, self.opc.JUMP_ABSOLUTE), pre_rtarget, True)))):
                                pass
                            else:
                                fix = None
                                jump_ifs = self.inst_matches(start, self.next_stmt[offset], self.opc.POP_JUMP_IF_FALSE)
                                last_jump_good = True
                                for j in jump_ifs:
                                    if target == self.get_target(j):
                                        if self.lines[j].next == j + 3 and last_jump_good:
                                            fix = j
                                            break
                                    else:
                                        last_jump_good = False

                                self.fixed_jumps[offset] = fix or match[(-1)]
                                return
                        else:
                            if self.version < 3.6:
                                self.fixed_jumps[offset] = match[(-1)]
                            elif target > offset:
                                self.fixed_jumps[offset] = target
                            return
                else:
                    next = self.next_stmt[offset]
                    if prev_op[next] == offset:
                        pass
                    elif self.is_jump_forward(next):
                        if target == self.get_target(next):
                            if code[prev_op[next]] == self.opc.POP_JUMP_IF_FALSE and (code[next] == self.opc.JUMP_FORWARD or target != rtarget or code[prev_op[pre_rtarget]] not in (self.opc.JUMP_ABSOLUTE, self.opc.RETURN_VALUE)):
                                self.fixed_jumps[offset] = prev_op[next]
                                return
                    elif code[next] == self.opc.JUMP_ABSOLUTE and self.is_jump_forward(target) and self.get_target(target) == self.get_target(next):
                        self.fixed_jumps[offset] = prev_op[next]
                        return
                if offset in self.ignore_if:
                    return
                rtarget_is_ja = code[pre_rtarget] == self.opc.JUMP_ABSOLUTE
                if rtarget_is_ja and pre_rtarget in self.stmts and pre_rtarget != offset and prev_op[pre_rtarget] != offset and not (code[rtarget] == self.opc.JUMP_ABSOLUTE and code[(rtarget + 3)] == self.opc.POP_BLOCK and code[prev_op[pre_rtarget]] != self.opc.JUMP_ABSOLUTE):
                    rtarget = pre_rtarget
                if self.version < 3.8:
                    rtarget_break = (
                     self.opc.RETURN_VALUE, self.opc.BREAK_LOOP)
                else:
                    rtarget_break = (
                     self.opc.RETURN_VALUE,)
                if self.is_jump_forward(pre_rtarget) or rtarget_is_ja and self.version >= 3.5:
                    if_end = self.get_target(pre_rtarget)
                    if if_end < pre_rtarget and self.version < 3.8 and code[prev_op[if_end]] == self.opc.SETUP_LOOP:
                        if if_end > start:
                            return
                    end = self.restrict_to_parent(if_end, parent)
                    self.structs.append({'type': 'if-then', 'start': start, 'end': pre_rtarget})
                    self.not_continue.add(pre_rtarget)
                    if rtarget < end and code[rtarget] not in (self.opc.END_FINALLY, self.opc.JUMP_ABSOLUTE) and code[prev_op[pre_rtarget]] not in (self.opc.POP_EXCEPT, self.opc.END_FINALLY):
                        self.structs.append({'type': 'else', 'start': rtarget, 'end': end})
                        self.else_start[rtarget] = end
                elif self.is_jump_back(pre_rtarget, 0):
                    if_end = rtarget
                    self.structs.append({'type': 'if-then', 'start': start, 'end': pre_rtarget})
                    self.not_continue.add(pre_rtarget)
                elif code[pre_rtarget] in rtarget_break:
                    self.structs.append({'type': 'if-then', 'start': start, 'end': rtarget})
                    jump_prev = prev_op[offset]
                    if self.is_pypy and code[jump_prev] == self.opc.COMPARE_OP:
                        if self.opc.cmp_op[code[(jump_prev + 1)]] == 'exception-match':
                            return
                    if self.version >= 3.5:
                        if self.version < 3.6 and code[rtarget] == self.opc.SETUP_EXCEPT:
                            return
                        next_op = rtarget
                        if code[next_op] == self.opc.POP_BLOCK:
                            next_op += instruction_size(self.code[next_op], self.opc)
                        if code[next_op] == self.opc.JUMP_ABSOLUTE:
                            next_op += instruction_size(self.code[next_op], self.opc)
                        if next_op in targets:
                            for try_op in targets[next_op]:
                                come_from_op = code[try_op]
                                if self.version < 3.8 and come_from_op == self.opc.SETUP_EXCEPT:
                                    return

                    if self.version >= 3.4:
                        self.fixed_jumps[offset] = rtarget
                    if code[pre_rtarget] == self.opc.RETURN_VALUE:
                        inst_index > 0 and self.insts[(inst_index - 1)].argval == 'exception-match' or self.return_end_ifs.add(pre_rtarget)
                else:
                    self.fixed_jumps[offset] = rtarget
                    self.not_continue.add(pre_rtarget)
            else:
                normal_jump = self.version >= 3.6
                if self.version == 3.5:
                    j = self.offset2inst_index[target]
                    if j + 2 < len(self.insts) and self.insts[(j + 2)].is_jump_target:
                        normal_jump = self.insts[(j + 1)].opname == 'POP_BLOCK'
                if normal_jump:
                    if target > offset:
                        self.fixed_jumps[offset] = target
                elif rtarget > offset:
                    self.fixed_jumps[offset] = rtarget
        elif self.version < 3.8 and op == self.opc.SETUP_EXCEPT:
            target = self.get_target(offset)
            end = self.restrict_to_parent(target, parent)
            self.fixed_jumps[offset] = end
        elif op == self.opc.POP_EXCEPT:
            next_offset = xdis.next_offset(op, self.opc, offset)
            target = self.get_target(next_offset)
            if target > next_offset:
                next_op = code[next_offset]
                if self.opc.JUMP_ABSOLUTE == next_op and self.opc.END_FINALLY != code[xdis.next_offset(next_op, self.opc, next_offset)]:
                    self.fixed_jumps[next_offset] = target
                    self.except_targets[target] = next_offset
        elif op == self.opc.SETUP_FINALLY:
            target = self.get_target(offset)
            end = self.restrict_to_parent(target, parent)
            self.fixed_jumps[offset] = end
        elif op in self.jump_if_pop:
            target = self.get_target(offset)
            if target > offset:
                unop_target = self.last_instr(offset, target, self.opc.JUMP_FORWARD, target)
                if unop_target and code[(unop_target + 3)] != self.opc.ROT_TWO:
                    self.fixed_jumps[offset] = unop_target
                else:
                    self.fixed_jumps[offset] = self.restrict_to_parent(target, parent)
        elif self.version >= 3.5:
            if op == self.opc.RETURN_VALUE:
                next_offset = xdis.next_offset(op, self.opc, offset)
                if next_offset < len(code) and code[next_offset] == self.opc.JUMP_ABSOLUTE and offset in self.return_end_ifs:
                    self.return_end_ifs.remove(offset)
            elif op == self.opc.JUMP_FORWARD:
                rtarget = self.get_target(offset)
                rtarget_prev = self.prev[rtarget]
                if code[rtarget_prev] == self.opc.RETURN_VALUE and rtarget_prev in self.return_end_ifs:
                    i = rtarget_prev
                    while i != offset:
                        if code[i] in [op3.JUMP_FORWARD, op3.JUMP_ABSOLUTE]:
                            return
                        i = self.prev[i]

                    self.return_end_ifs.remove(rtarget_prev)
        return

    def is_jump_back(self, offset, extended_arg):
        """
        Return True if the code at offset is some sort of jump back.
        That is, it is ether "JUMP_FORWARD" or an absolute jump that
        goes forward.
        """
        if self.code[offset] != self.opc.JUMP_ABSOLUTE:
            return False
        return offset > self.get_target(offset, extended_arg)

    def next_except_jump(self, start):
        """
        Return the next jump that was generated by an except SomeException:
        construct in a try...except...else clause or None if not found.
        """
        if self.code[start] == self.opc.DUP_TOP:
            except_match = self.first_instr(start, len(self.code), self.opc.POP_JUMP_IF_FALSE)
            if except_match:
                jmp = self.prev_op[self.get_target(except_match)]
                self.ignore_if.add(except_match)
                self.not_continue.add(jmp)
                return jmp
        count_END_FINALLY = 0
        count_SETUP_ = 0
        for i in self.op_range(start, len(self.code)):
            op = self.code[i]
            if op == self.opc.END_FINALLY:
                if count_END_FINALLY == count_SETUP_:
                    assert self.code[self.prev_op[i]] in frozenset([self.opc.JUMP_ABSOLUTE, self.opc.JUMP_FORWARD, self.opc.RETURN_VALUE])
                    self.not_continue.add(self.prev_op[i])
                    return self.prev_op[i]
                count_END_FINALLY += 1
            elif op in self.setup_opts_no_loop:
                count_SETUP_ += 1

    def rem_or(self, start, end, instr, target=None, include_beyond_target=False):
        """
        Find offsets of all requested <instr> between <start> and <end>,
        optionally <target>ing specified offset, and return list found
        <instr> offsets which are not within any POP_JUMP_IF_TRUE jumps.
        """
        assert start >= 0 and end <= len(self.code) and start <= end
        instr_offsets = self.inst_matches(start, end, instr, target, include_beyond_target)
        if self.version == 3.0:
            jump_true_op = self.opc.JUMP_IF_TRUE
        else:
            jump_true_op = self.opc.POP_JUMP_IF_TRUE
        pjit_offsets = self.inst_matches(start, end, jump_true_op)
        filtered = []
        for pjit_offset in pjit_offsets:
            pjit_tgt = self.get_target(pjit_offset) - 3
            for instr_offset in instr_offsets:
                if instr_offset <= pjit_offset or instr_offset >= pjit_tgt:
                    filtered.append(instr_offset)

            instr_offsets = filtered
            filtered = []

        return instr_offsets


if __name__ == '__main__':
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION >= 3.2:
        import inspect
        co = inspect.currentframe().f_code
        from uncompyle6 import PYTHON_VERSION
        (tokens, customize) = Scanner3(PYTHON_VERSION).ingest(co)
        for t in tokens:
            print t

    else:
        print 'Need to be Python 3.2 or greater to demo; I am %s.' % PYTHON_VERSION