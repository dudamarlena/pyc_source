# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/bytecode.py
# Compiled at: 2015-05-17 09:17:03
"""Bytecode instruction routines"""
import dis, re
from opcode import opname, HAVE_ARGUMENT

def op_at_code_loc(code, loc):
    try:
        op = ord(code[loc])
    except IndexError:
        return 'got IndexError'

    return opname[op]


def op_at_frame(frame, loc=None):
    code = frame.f_code.co_code
    if loc is None:
        loc = frame.f_lasti
    return op_at_code_loc(code, loc)


def next_opcode(code, offset):
    """Return the next opcode and offset as a tuple. Tuple (-100,
    -1000) is returned when reaching the end."""
    n = len(code)
    while offset < n:
        c = code[offset]
        op = ord(c)
        offset += 1
        if op >= HAVE_ARGUMENT:
            offset += 2
        yield (
         op, offset)

    yield (-100, -1000)


def next_linestart(co, offset, count=1):
    linestarts = dict(dis.findlinestarts(co))
    code = co.co_code
    for (op, offset) in next_opcode(code, offset):
        if offset in linestarts:
            count -= 1
            if 0 == count:
                return linestarts[offset]

    return -1000


def stmt_contains_opcode(co, lineno, query_opcode):
    linestarts = dict(dis.findlinestarts(co))
    code = co.co_code
    found_start = False
    for (offset, start_line) in list(linestarts.items()):
        if start_line == lineno:
            found_start = True
            break

    if not found_start:
        return False
    for (op, offset) in next_opcode(code, offset):
        if -1000 == offset or linestarts.get(offset):
            return False
        opcode = opname[op]
        if query_opcode == opcode:
            return True

    return False


_re_def_str = '^\\s*def\\s'
_re_def = re.compile(_re_def_str)

def is_def_stmt(line, frame):
    """Return True if we are looking at a def statement"""
    return line and _re_def.match(line) and op_at_frame(frame) == 'LOAD_CONST' and stmt_contains_opcode(frame.f_code, frame.f_lineno, 'MAKE_FUNCTION')


_re_class = re.compile('^\\s*class\\s')

def is_class_def(line, frame):
    """Return True if we are looking at a class definition statement"""
    return line and _re_class.match(line) and stmt_contains_opcode(frame.f_code, frame.f_lineno, 'BUILD_CLASS')


if __name__ == '__main__':
    import inspect

    def sqr(x):
        return x * x


    frame = inspect.currentframe()
    co = frame.f_code
    lineno = frame.f_lineno
    print 'contains MAKE_FUNCTION %s' % stmt_contains_opcode(co, lineno - 4, 'MAKE_FUNCTION')
    print 'contains MAKE_FUNCTION %s' % stmt_contains_opcode(co, lineno, 'MAKE_FUNCTION')

    def double(x):
        dis.dis(double)
        eval('1+2')
        frame = inspect.currentframe()
        co = frame.f_code
        lineno = frame.f_lineno
        print 'contains CALL_FUNCTION %s' % stmt_contains_opcode(co, lineno - 2, 'CALL_FUNCTION')
        return x + x


    double(2)
    print 'op at frame: %s' % op_at_frame(frame)
    print 'op at frame, position 2: %s' % op_at_frame(frame, 2)
    print 'def statement: x=5?: %s' % is_def_stmt('x=5', frame)
    print is_def_stmt('def foo():', frame)

    class Foo:
        pass


    lineno = frame.f_lineno
    print 'contains BUILD_CLASS %s' % stmt_contains_opcode(co, lineno - 2, 'BUILD_CLASS')
    print 'contains BUILD_CLASS %s' % stmt_contains_opcode(co, lineno, 'BUILD_CLASS')