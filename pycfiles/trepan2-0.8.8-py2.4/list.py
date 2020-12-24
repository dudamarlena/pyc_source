# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/list.py
# Compiled at: 2018-06-25 10:54:26
import inspect, os, linecache, pyficache, sys
from pygments.console import colorize
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor.cmdlist import parse_list_cmd
from trepan.lib.deparse import deparse_and_cache

class ListCommand(Mbase_cmd.DebuggerCommand):
    """**list** [ *range* ]

**list**  **+** | **-** | **.**

List source code. See `help syntax range` for what can go in a list range.

Without arguments, print lines starting from where the last list left off
since the last entry to the debugger. We start off at the location indicated
by the current stack.

in addition you can also use:

  - a '.' for the location of the current frame
  - a '-' for the lines before the last list
  - a '+' for the lines after the last list

Examples:
--------

    list 5               # List starting from line 5 of current file
    list 5 ,             # Same as above.
    list , 5             # list listsize lines before and up to 5
    list foo.py:5        # List starting from line 5 of file foo.py
    list foo()           # List starting from function foo
    list os.path:5       # List starting from line 5 of module os.path
    list os.path:5, 6    # list lines 5 and 6 of os.path
    list os.path:5, +1   # Same as above. +1 is an offset
    list os.path:5, 1    # Same as above, since 1 < 5.
    list os.path:5, +6   # list lines 5-11
    list os.path.join()  # List lines centered around the os.join.path function.
    list .               # List lines centered from where we currently are stopped
    list -               # List lines previous to those just shown
    list                 # List continuing from where we last left off

See also:
---------

`set listize` or `show listsize` to see or set the value; `help syntax location`
for the specification of a location and `help syntax range` for the specification
of a range.
"""
    __module__ = __name__
    aliases = ('l', )
    category = 'files'
    min_args = 0
    max_args = 3
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'List source code'

    def run(self, args):
        proc = self.proc
        dbg_obj = self.core.debugger
        listsize = dbg_obj.settings['listsize']
        (filename, first, last) = parse_list_cmd(proc, args, listsize)
        curframe = proc.curframe
        if filename is None:
            return
        show_marks = True
        filename = pyficache.unmap_file(pyficache.pyc2py(filename))
        if filename == '<string>' and proc.curframe.f_code:
            co = proc.curframe.f_code
            (temp_filename, name_for_code) = deparse_and_cache(co, proc.errmsg)
            if temp_filename:
                filename = temp_filename
                show_marks = False
        max_line = pyficache.size(filename)
        if max_line is None:
            self.errmsg('No file %s found; using "deparse" command instead to show source' % filename)
            proc.commands['deparse'].run(['deparse'])
            return
        canonic_filename = os.path.realpath(os.path.normcase(filename))
        if first > max_line:
            self.errmsg('Bad start line %d - file "%s" has only %d lines' % (first, filename, max_line))
            return
        if last > max_line:
            self.msg('End position changed to last line %d ' % max_line)
            last = max_line
        bplist = self.core.bpmgr.bplist
        opts = {'reload_on_change': self.settings['reload'], 'output': self.settings['highlight'], 'strip_nl': False}
        if 'style' in self.settings:
            opts['style'] = self.settings['style']
        if first <= 0:
            first = 1
        try:
            for lineno in range(first, last + 1):
                line = pyficache.getline(filename, lineno, opts)
                if line is None:
                    line = linecache.getline(filename, lineno, proc.frame.f_globals)
                if line is None:
                    self.msg('[EOF]')
                    break
                else:
                    line = line.rstrip('\n')
                    s = proc._saferepr(lineno).rjust(3)
                    if len(s) < 5:
                        s += ' '
                    if show_marks and (canonic_filename, lineno) in list(bplist.keys()):
                        bp = bplist[(canonic_filename, lineno)][0]
                        a_pad = '%02d' % bp.number
                        s += bp.icon_char()
                    else:
                        s += ' '
                        a_pad = '  '
                    if curframe and lineno == inspect.getlineno(curframe) and show_marks:
                        s += '->'
                        if 'plain' != self.settings['highlight']:
                            s = colorize('bold', s)
                    else:
                        s += a_pad
                    self.msg(s + '\t' + line)
                    proc.list_lineno = lineno

        except KeyboardInterrupt:
            pass

        return False


if __name__ == '__main__':

    def doit(cmd, args):
        proc = cmd.proc
        proc.current_command = (' ').join(args)
        cmd.run(args)


    from trepan.processor.command import mock as Mmock
    from trepan.processor.cmdproc import CommandProcessor
    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    cmdproc.frame = sys._getframe()
    cmdproc.setup()
    lcmd = ListCommand(cmdproc)
    print '--' * 10

    def foo():
        return 'bar'


    doit(lcmd, ['list', '40,', '60'])