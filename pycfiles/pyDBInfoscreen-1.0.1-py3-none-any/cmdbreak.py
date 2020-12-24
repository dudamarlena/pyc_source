# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/cmdbreak.py
# Compiled at: 2013-01-04 05:13:40
import inspect, os, pyficache
from import_relative import import_relative
Mmisc = import_relative('misc', '..')

def set_break(cmd_obj, func, filename, lineno, condition, temporary, args):
    if lineno is None:
        part1 = "I don't understand '%s' as a line number, function name," % (' ').join(args[1:])
        msg = Mmisc.wrapped_lines(part1, 'or file/module plus line number.', cmd_obj.settings['width'])
        cmd_obj.errmsg(msg)
        return False
    if filename is None:
        filename = cmd_obj.proc.curframe.f_code.co_filename
        filename = cmd_obj.core.canonic(filename)
    if func is None:
        ok_linenos = pyficache.trace_line_numbers(filename)
        if not ok_linenos or lineno not in ok_linenos:
            part1 = 'File %s' % cmd_obj.core.filename(filename)
            msg = Mmisc.wrapped_lines(part1, 'is not stoppable at line %d.' % lineno, cmd_obj.settings['width'])
            cmd_obj.errmsg(msg)
            return False
    bp = cmd_obj.core.bpmgr.add_breakpoint(filename, lineno, temporary, condition, func)
    if func:
        cmd_obj.msg('Breakpoint %d set on calling function %s()' % (bp.number, func.func_name))
        part1 = 'Currently this is line %d of file' % lineno
        msg = Mmisc.wrapped_lines(part1, cmd_obj.core.filename(filename), cmd_obj.settings['width'])
    else:
        part1 = 'Breakpoint %d set at line %d of file' % (bp.number, lineno)
        msg = Mmisc.wrapped_lines(part1, cmd_obj.core.filename(filename), cmd_obj.settings['width'])
    cmd_obj.msg(msg)
    return True


def parse_break_cmd(cmd_obj, args):
    curframe = cmd_obj.proc.curframe
    if 0 == len(args) or args[0] == 'if':
        filename = cmd_obj.core.canonic(curframe.f_code.co_filename)
        lineno = curframe.f_lineno
        if 0 == len(args):
            return (None, filename, lineno, None)
        modfunc = None
        condition_pos = 0
    else:
        (modfunc, filename, lineno) = cmd_obj.proc.parse_position(args[0])
        condition_pos = 1
    if inspect.ismodule(modfunc) and lineno is None and len(args) > 1:
        val = cmd_obj.proc.get_an_int(args[1], 'Line number expected, got %s.' % args[1])
        if val is None:
            return (None, None, None, None)
        lineno = val
        condition_pos = 2
    if len(args) > condition_pos and 'if' == args[condition_pos]:
        condition = (' ').join(args[condition_pos + 1:])
    else:
        condition = None
    if inspect.isfunction(modfunc):
        func = modfunc
    else:
        func = None
    return (func, filename, lineno, condition)