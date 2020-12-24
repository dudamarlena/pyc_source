# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanner.py
# Compiled at: 2020-04-27 23:06:35
"""
scanner/ingestion module. From here we call various version-specific
scanners, e.g. for Python 2.7 or 3.4.
"""
from array import array
import sys
from uncompyle6 import PYTHON3, IS_PYPY, PYTHON_VERSION
from uncompyle6.scanners.tok import Token
import xdis
from xdis.bytecode import Bytecode, instruction_size, extended_arg_val, next_offset
from xdis.magics import canonic_python_version
from xdis.util import code2num
if PYTHON_VERSION < 2.6:
    from xdis.namedtuple24 import namedtuple
else:
    from collections import namedtuple
PYTHON_VERSIONS = frozenset((1.0, 1.1, 1.3, 1.4, 1.5, 1.6, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9))
CANONIC2VERSION = dict(((canonic_python_version[str(v)], v) for v in PYTHON_VERSIONS))
CANONIC2VERSION['3.5.2'] = 3.5
if PYTHON3:
    intern = sys.intern
    L65536 = 65536

    def long(l):
        return l


else:
    L65536 = long(65536)

class Code(object):
    """
    Class for representing code-objects.

    This is similar to the original code object, but additionally
    the diassembled code is stored in the attribute '_tokens'.
    """
    __module__ = __name__

    def __init__(self, co, scanner, classname=None):
        for i in dir(co):
            if i.startswith('co_'):
                setattr(self, i, getattr(co, i))

        (self._tokens, self._customize) = scanner.ingest(co, classname)


class Scanner(object):
    __module__ = __name__

    def __init__(self, version, show_asm=None, is_pypy=False):
        self.version = version
        self.show_asm = show_asm
        self.is_pypy = is_pypy
        if version in PYTHON_VERSIONS:
            if is_pypy:
                v_str = 'opcode_%spypy' % int(version * 10)
            else:
                v_str = 'opcode_%s' % int(version * 10)
            exec 'from xdis.opcodes import %s' % v_str
            exec 'self.opc = %s' % v_str
        else:
            raise TypeError('%s is not a Python version I know about' % version)
        self.opname = self.opc.opname
        self.resetTokenClass()

    def build_instructions(self, co):
        """
        Create a list of instructions (a structured object rather than
        an array of bytes) and store that in self.insts
        """
        self.code = array('B', co.co_code)
        bytecode = Bytecode(co, self.opc)
        self.build_prev_op()
        self.insts = self.remove_extended_args(list(bytecode))
        self.lines = self.build_lines_data(co)
        self.offset2inst_index = {}
        for (i, inst) in enumerate(self.insts):
            self.offset2inst_index[inst.offset] = i

        return bytecode

    def build_lines_data(self, code_obj):
        """
        Generate various line-related helper data.
        """
        if self.version > 1.4:
            linestarts = list(self.opc.findlinestarts(code_obj))
        else:
            linestarts = [
             [
              0, 1]]
        self.linestarts = dict(linestarts)
        lines = []
        LineTuple = namedtuple('LineTuple', ['l_no', 'next'])
        (_, prev_line_no) = linestarts[0]
        offset = 0
        for (start_offset, line_no) in linestarts[1:]:
            while offset < start_offset:
                lines.append(LineTuple(prev_line_no, start_offset))
                offset += 1

            prev_line_no = line_no

        codelen = len(self.code)
        while offset < codelen:
            lines.append(LineTuple(prev_line_no, codelen))
            offset += 1

        return lines

    def build_prev_op(self):
        """
        Compose 'list-map' which allows to jump to previous
        op, given offset of current op as index.
        """
        code = self.code
        codelen = len(code)
        self.prev = self.prev_op = [
         0]
        for offset in self.op_range(0, codelen):
            op = code[offset]
            for _ in range(instruction_size(op, self.opc)):
                self.prev_op.append(offset)

    def is_jump_forward(self, offset):
        """
        Return True if the code at offset is some sort of jump forward.
        That is, it is ether "JUMP_FORWARD" or an absolute jump that
        goes forward.
        """
        opname = self.get_inst(offset).opname
        if opname == 'JUMP_FORWARD':
            return True
        if opname != 'JUMP_ABSOLUTE':
            return False
        return offset < self.get_target(offset)

    def prev_offset(self, offset):
        return self.insts[(self.offset2inst_index[offset] - 1)].offset

    def get_inst(self, offset):
        if offset not in self.offset2inst_index:
            offset -= instruction_size(self.opc.EXTENDED_ARG, self.opc)
            assert self.code[offset] == self.opc.EXTENDED_ARG
        return self.insts[self.offset2inst_index[offset]]

    def get_target(self, offset, extended_arg=0):
        """
        Get next instruction offset for op located at given <offset>.
        NOTE: extended_arg is no longer used
        """
        inst = self.get_inst(offset)
        if inst.opcode in self.opc.JREL_OPS | self.opc.JABS_OPS:
            target = inst.argval
        else:
            target = next_offset(inst.opcode, self.opc, inst.offset)
        return target

    def get_argument(self, pos):
        arg = self.code[(pos + 1)] + self.code[(pos + 2)] * 256
        return arg

    def next_offset(self, op, offset):
        return xdis.next_offset(op, self.opc, offset)

    def print_bytecode(self):
        for i in self.op_range(0, len(self.code)):
            op = self.code[i]
            if op in self.JUMP_OPS:
                dest = self.get_target(i, op)
                print '%i\t%s\t%i' % (i, self.opname[op], dest)
            else:
                print '%i\t%s\t' % (i, self.opname[op])

    def first_instr(self, start, end, instr, target=None, exact=True):
        """
        Find the first <instr> in the block from start to end.
        <instr> is any python bytecode instruction or a list of opcodes
        If <instr> is an opcode with a target (like a jump), a target
        destination can be specified which must match precisely if exact
        is True, or if exact is False, the instruction which has a target
        closest to <target> will be returned.

        Return index to it or None if not found.
        """
        code = self.code
        assert start >= 0 and end <= len(code)
        if not isinstance(instr, list):
            instr = [
             instr]
        result_offset = None
        current_distance = len(code)
        for offset in self.op_range(start, end):
            op = code[offset]
            if op in instr:
                if target is None:
                    return offset
                dest = self.get_target(offset)
                if dest == target:
                    return offset
                elif not exact:
                    new_distance = abs(target - dest)
                    if new_distance < current_distance:
                        current_distance = new_distance
                        result_offset = offset

        return result_offset

    def last_instr(self, start, end, instr, target=None, exact=True):
        """
        Find the last <instr> in the block from start to end.
        <instr> is any python bytecode instruction or a list of opcodes
        If <instr> is an opcode with a target (like a jump), a target
        destination can be specified which must match precisely if exact
        is True, or if exact is False, the instruction which has a target
        closest to <target> will be returned.

        Return index to it or None if not found.
        """
        code = self.code
        if not (start >= 0 and end <= len(code)):
            return
        if not isinstance(instr, list):
            instr = [
             instr]
        result_offset = None
        current_distance = self.insts[(-1)].offset - self.insts[0].offset
        extended_arg = 0
        for offset in self.op_range(start, end):
            op = code[offset]
            if op == self.opc.EXTENDED_ARG:
                arg = code2num(code, offset + 1) | extended_arg
                extended_arg = extended_arg_val(self.opc, arg)
                continue
            if op in instr:
                if target is None:
                    result_offset = offset
                else:
                    dest = self.get_target(offset, extended_arg)
                    if dest == target:
                        current_distance = 0
                        result_offset = offset
                    elif not exact:
                        new_distance = abs(target - dest)
                        if new_distance <= current_distance:
                            current_distance = new_distance
                            result_offset = offset
            extended_arg = 0

        return result_offset

    def inst_matches(self, start, end, instr, target=None, include_beyond_target=False):
        """
        Find all `instr` in the block from start to end.
        `instr` is a Python opcode or a list of opcodes
        If `instr` is an opcode with a target (like a jump), a target
        destination can be specified which must match precisely.

        Return a list with indexes to them or [] if none found.
        """
        try:
            None in instr
        except:
            instr = [
             instr]

        first = self.offset2inst_index[start]
        result = []
        for inst in self.insts[first:]:
            if inst.opcode in instr:
                if target is None:
                    result.append(inst.offset)
                else:
                    t = self.get_target(inst.offset)
                    if include_beyond_target:
                        if t >= target:
                            result.append(inst.offset)
                        elif t == target:
                            result.append(inst.offset)
            elif inst.offset >= end:
                break

        return result

    def all_instr(self, start, end, instr, target=None, include_beyond_target=False):
        """
        Find all `instr` in the block from start to end.
        `instr` is any Python opcode or a list of opcodes
        If `instr` is an opcode with a target (like a jump), a target
        destination can be specified which must match precisely.

        Return a list with indexes to them or [] if none found.
        """
        code = self.code
        assert start >= 0 and end <= len(code)
        try:
            None in instr
        except:
            instr = [
             instr]

        result = []
        extended_arg = 0
        for offset in self.op_range(start, end):
            op = code[offset]
            if op == self.opc.EXTENDED_ARG:
                arg = code2num(code, offset + 1) | extended_arg
                extended_arg = extended_arg_val(self.opc, arg)
                continue
            if op in instr:
                if target is None:
                    result.append(offset)
                else:
                    t = self.get_target(offset, extended_arg)
                    if include_beyond_target and t >= target:
                        result.append(offset)
                    elif t == target:
                        result.append(offset)
            extended_arg = 0

        return result

    def opname_for_offset(self, offset):
        return self.opc.opname[self.code[offset]]

    def op_name(self, op):
        return self.opc.opname[op]

    def op_range(self, start, end):
        """
        Iterate through positions of opcodes, skipping
        arguments.
        """
        while start < end:
            yield start
            start += instruction_size(self.code[start], self.opc)

    def remove_extended_args(self, instructions):
        """Go through instructions removing extended ARG.
        get_instruction_bytes previously adjusted the operand values
        to account for these"""
        new_instructions = []
        last_was_extarg = False
        n = len(instructions)
        for (i, inst) in enumerate(instructions):
            if inst.opname == 'EXTENDED_ARG' and i + 1 < n and instructions[(i + 1)].opname != 'MAKE_FUNCTION':
                last_was_extarg = True
                starts_line = inst.starts_line
                is_jump_target = inst.is_jump_target
                offset = inst.offset
                continue
            if last_was_extarg:
                new_inst = inst._replace(starts_line=starts_line, is_jump_target=is_jump_target, offset=offset)
                inst = new_inst
                if i < n:
                    new_prev = self.prev_op[instructions[i].offset]
                    j = instructions[(i + 1)].offset
                    old_prev = self.prev_op[j]
                    while self.prev_op[j] == old_prev and j < n:
                        self.prev_op[j] = new_prev
                        j += 1

            last_was_extarg = False
            new_instructions.append(inst)

        return new_instructions

    def remove_mid_line_ifs(self, ifs):
        """
        Go through passed offsets, filtering ifs
        located somewhere mid-line.
        """
        filtered = []
        for i in ifs:
            if self.lines[i].l_no == self.lines[(i + 3)].l_no:
                if self.code[self.prev[self.lines[i].next]] in (self.opc.PJIT, self.opc.PJIF):
                    continue
            filtered.append(i)

        return filtered

    def resetTokenClass(self):
        return self.setTokenClass(Token)

    def restrict_to_parent(self, target, parent):
        """Restrict target to parent structure boundaries."""
        if not parent['start'] < target < parent['end']:
            target = parent['end']
        return target

    def setTokenClass(self, tokenClass):
        self.Token = tokenClass
        return self.Token


def parse_fn_counts(argc):
    return (
     argc & 255, argc >> 8 & 255, argc >> 16 & 32767)


def get_scanner(version, is_pypy=False, show_asm=None):
    if isinstance(version, str):
        if version not in canonic_python_version:
            raise RuntimeError('Unknown Python version in xdis %s' % version)
        canonic_version = canonic_python_version[version]
        if canonic_version not in CANONIC2VERSION:
            raise RuntimeError('Unsupported Python version %s (canonic %s)' % (version, canonic_version))
        version = CANONIC2VERSION[canonic_version]
    if version in PYTHON_VERSIONS:
        v_str = '%s' % int(version * 10)
        try:
            import importlib
            if is_pypy:
                scan = importlib.import_module('uncompyle6.scanners.pypy%s' % v_str)
            else:
                scan = importlib.import_module('uncompyle6.scanners.scanner%s' % v_str)
            if False:
                print scan
        except ImportError:
            if is_pypy:
                exec ('import uncompyle6.scanners.pypy%s as scan' % v_str, locals(), globals())
            else:
                exec (
                 'import uncompyle6.scanners.scanner%s as scan' % v_str, locals(), globals())
        else:
            if is_pypy:
                scanner = eval('scan.ScannerPyPy%s(show_asm=show_asm)' % v_str, locals(), globals())
            else:
                scanner = eval('scan.Scanner%s(show_asm=show_asm)' % v_str, locals(), globals())
    else:
        raise RuntimeError('Unsupported Python version %s' % version)
    return scanner


if __name__ == '__main__':
    import inspect, uncompyle6
    co = inspect.currentframe().f_code
    scanner = get_scanner(uncompyle6.PYTHON_VERSION, IS_PYPY, True)
    (tokens, customize) = scanner.ingest(co, {}, show_asm='after')