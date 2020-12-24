# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/cmd_addrlist.py
# Compiled at: 2017-11-02 15:38:09
from trepan.processor.parse.semantics import build_arange, Location
from trepan.processor.parse.parser import LocationError
from trepan.processor.parse.scanner import ScannerError
from trepan.processor.location import resolve_address_location
INVALID_PARSE_LIST = (None, None, None, None, None, None)

def parse_addr_list_cmd(proc, args, listsize=40):
    """Parses arguments for the "list" command and returns the tuple:
    (filename, first line number, last line number)
    or sets these to None if there was some problem."""
    text = proc.current_command[len(args[0]) + 1:].strip()
    if text in frozenset(('', '.', '+', '-')):
        if text == '.':
            location = resolve_address_location(proc, '.')
            return (
             location.path, location.line_number, True,
             location.line_number + listsize, True,
             location.method)
        if proc.list_offset is None:
            proc.errmsg("Don't have previous list location")
            return INVALID_PARSE_LIST
        filename = proc.list_filename
        if text == '+':
            first = max(0, proc.list_offset - 1)
        else:
            if text == '-':
                if proc.list_lineno == 1 + listsize:
                    proc.errmsg('Already at start of %s.' % proc.list_filename)
                    return INVALID_PARSE_LIST
                first = max(1, proc.list_lineno - 2 * listsize - 1)
            elif text == '':
                first = proc.list_offset + 1
                last = first + listsize - 1
                return (
                 filename, first, True, last, True, proc.list_object)
        last = first + listsize - 1
        return (
         filename, first, True, last, True, proc.list_object)
    else:
        try:
            list_range = build_arange(text)
        except LocationError as e:
            proc.errmsg('Error in parsing list range at or around:')
            proc.errmsg(e.text)
            proc.errmsg(e.text_cursor)
            return INVALID_PARSE_LIST
        except ScannerError as e:
            proc.errmsg('Lexical error in parsing list range at or around:')
            proc.errmsg(e.text)
            proc.errmsg(e.text_cursor)
            return INVALID_PARSE_LIST

        if list_range.first is None:
            assert isinstance(list_range.last, Location)
            location = resolve_address_location(proc, list_range.last)
            if not location:
                return INVALID_PARSE_LIST
            last = location.line_number
            if location.is_address:
                raise RuntimeError("We don't handle ending offsets")
        else:
            first = max(1, last - listsize)
        return (location.path, first, False, last, False, location.method)
    if isinstance(list_range.first, int):
        first = list_range.first
        location = resolve_address_location(proc, list_range.last)
        if not location:
            return INVALID_PARSE_LIST
        filename = location.path
        last = location.line_number
        if not location.is_address and last < first:
            last = first + last
        return (location.path, first, False, last, location.is_address, location.method)
    else:
        assert isinstance(list_range.first, Location)
        location = resolve_address_location(proc, list_range.first)
        if not location:
            return INVALID_PARSE_LIST
        else:
            first = location.line_number
            first_is_addr = location.is_address
            last_is_addr = False
            last = list_range.last
            if isinstance(last, str):
                assert last[0] in ('+', '*')
                last_is_addr = last[0] == '*'
                if last_is_addr:
                    last = int(last[1:])
                else:
                    last = first + int(last[1:])
            else:
                if not last:
                    last_is_addr = True
                    last = first + listsize
                elif last < first:
                    last = first + last
            return (
             location.path, first, first_is_addr, last, last_is_addr, location.method)
        return


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    from trepan.processor.cmdproc import CommandProcessor
    import sys
    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    cmdproc.frame = sys._getframe()
    cmdproc.setup()

    def five():
        return 5


    import os
    for cmd in ('disasm *5, *10', 'disasm *15, 10', 'disasm five(), *10'):
        args = cmd.split(' ')
        cmdproc.current_command = cmd
        print(parse_addr_list_cmd(cmdproc, args))