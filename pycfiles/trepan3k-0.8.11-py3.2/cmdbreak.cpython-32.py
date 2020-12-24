# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/cmdbreak.py
# Compiled at: 2018-05-18 19:47:35
import inspect, pyficache
from trepan import misc as Mmisc
from trepan.processor.parse.semantics import build_bp_expr
from trepan.processor.parse.parser import LocationError
from trepan.processor.parse.scanner import ScannerError
from trepan.processor.location import resolve_location

def set_break(cmd_obj, func, filename, lineno, condition, temporary, args, force=False):
    if lineno is None:
        part1 = "I don't understand '%s' as a line number, function name," % ' '.join(args[1:])
        msg = Mmisc.wrapped_lines(part1, 'or file/module plus line number.', cmd_obj.settings['width'])
        cmd_obj.errmsg(msg)
        return False
    else:
        if filename is None:
            filename = cmd_obj.proc.curframe.f_code.co_filename
            filename = cmd_obj.core.canonic(filename)
        if func is None:
            ok_linenos = pyficache.trace_line_numbers(filename)
            if not ok_linenos or lineno not in ok_linenos:
                part1 = 'File %s' % cmd_obj.core.filename(filename)
                msg = Mmisc.wrapped_lines(part1, 'is not stoppable at line %d.' % lineno, cmd_obj.settings['width'])
                cmd_obj.errmsg(msg)
                if force:
                    cmd_obj.msg('Breakpoint set although it may never be reached')
                else:
                    return False
        bp = cmd_obj.core.bpmgr.add_breakpoint(filename, lineno, temporary, condition, func)
        if func and inspect.isfunction(func):
            cmd_obj.msg('Breakpoint %d set on calling function %s()' % (
             bp.number, func.__name__))
            part1 = 'Currently this is line %d of file' % lineno
            msg = Mmisc.wrapped_lines(part1, cmd_obj.core.filename(filename), cmd_obj.settings['width'])
        else:
            part1 = 'Breakpoint %d set at line %d of file' % (
             bp.number, lineno)
            msg = Mmisc.wrapped_lines(part1, cmd_obj.core.filename(filename), cmd_obj.settings['width'])
        cmd_obj.msg(msg)
        return True


INVALID_PARSE_BREAK = (None, None, None, None)

def parse_break_cmd(proc, args):
    if proc.current_command is None:
        proc.errmsg('Internal error')
        return INVALID_PARSE_BREAK
    else:
        text = proc.current_command[len(args[0]) + 1:]
        if len(args) > 1 and args[1] == 'if':
            location = '.'
            condition = text[text.find('if ') + 3:]
        else:
            if text == '':
                location = '.'
                condition = None
            else:
                try:
                    bp_expr = build_bp_expr(text)
                except LocationError as e:
                    proc.errmsg('Error in parsing breakpoint expression at or around:')
                    proc.errmsg(e.text)
                    proc.errmsg(e.text_cursor)
                    return INVALID_PARSE_BREAK
                except ScannerError as e:
                    proc.errmsg('Lexical error in parsing breakpoint expression at or around:')
                    proc.errmsg(e.text)
                    proc.errmsg(e.text_cursor)
                    return INVALID_PARSE_BREAK

                location = bp_expr.location
                condition = bp_expr.condition
        location = resolve_location(proc, location)
        if location:
            return (location.method, location.path, location.line_number, condition)
        else:
            return INVALID_PARSE_BREAK
        return


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    from trepan.processor.cmdproc import CommandProcessor
    import sys
    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    cmdproc.frame = sys._getframe()
    cmdproc.setup()
    for cmd in ('break 4 if i==5', ):
        args = cmd.split(' ')
        cmdproc.current_command = cmd
        print(parse_break_cmd(cmdproc, args))