# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/list.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 8910 bytes
import inspect, os, linecache, pyficache, sys, re
from pygments.console import colorize
from trepan.lib import stack as Mstack
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor.cmdlist import parse_list_cmd
from trepan.processor import cmdproc as Mcmdproc
from trepan.lib.deparse import deparse_and_cache
from pyficache import pyc2py

class ListCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**list** [ *range* ]\n\n**list**  **+** | **-** | **.**\n\nList source code. See `help syntax range` for what can go in a list range.\n\nWithout arguments, print lines starting from where the last list left off\nsince the last entry to the debugger. We start off at the location indicated\nby the current stack.\n\nin addition you can also use:\n\n  - a '.' for the location of the current frame\n  - a '-' for the lines before the last list\n  - a '+' for the lines after the last list\n\nExamples:\n--------\n\n    list 5               # List starting from line 5 of current file\n    list 5 ,             # Same as above.\n    list , 5             # list listsize lines before and up to 5\n    list foo.py:5        # List starting from line 5 of file foo.py\n    list foo()           # List starting from function foo\n    list os.path:5       # List starting from line 5 of module os.path\n    list os.path:5, 6    # list lines 5 and 6 of os.path\n    list os.path:5, +1   # Same as above. +1 is an offset\n    list os.path:5, 1    # Same as above, since 1 < 5.\n    list os.path:5, +6   # list lines 5-11\n    list os.path.join()  # List lines centered around the os.join.path function.\n    list .               # List lines centered from where we currently are stopped\n    list -               # List lines previous to those just shown\n    list                 # List continuing from where we last left off\n\nSee also:\n---------\n\n`set listize` or `show listsize` to see or set the value; `help syntax location`\nfor the specification of a location and `help syntax range` for the specification\nof a range.\n"
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
        filename, first, last = parse_list_cmd(proc, args, listsize)
        curframe = proc.curframe
        show_marks = True
        if filename is None:
            return
        else:
            if filename == '<string>':
                if proc.curframe.f_code:
                    co = proc.curframe.f_code
                    temp_filename, name_for_code = deparse_and_cache(co, proc.errmsg)
                    if temp_filename:
                        filename = temp_filename
                        show_marks = False
            m = re.search('^<frozen (.*)>', filename)
            if m and m.group(1):
                filename = m.group(1)
                canonic_filename = pyficache.unmap_file(filename)
            else:
                filename = pyc2py(filename)
                canonic_filename = os.path.realpath(os.path.normcase(filename))
            max_line = pyficache.size(filename)
            if max_line is None:
                self.errmsg('No file %s found; using "deparse" command instead to show source' % filename)
                proc.commands['deparse'].run(['deparse'])
                return
            if first > max_line:
                self.errmsg('Bad start line %d - file "%s" has only %d lines' % (
                 first, filename, max_line))
                return
            if last > max_line:
                self.msg('End position changed to last line %d ' % max_line)
                last = max_line
            bplist = self.core.bpmgr.bplist
            opts = {'reload_on_change': self.settings['reload'], 
             'output': self.settings['highlight'], 
             'strip_nl': False}
            if 'style' in self.settings:
                opts['style'] = self.settings['style']
            try:
                match, reason = Mstack.check_path_with_frame(curframe, filename)
                if not match:
                    if filename not in Mcmdproc.warned_file_mismatches:
                        self.errmsg(reason)
                        Mcmdproc.warned_file_mismatches.add(filename)
            except:
                pass

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
                        if show_marks and (
                         canonic_filename, lineno) in list(bplist.keys()):
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
                        self.proc.list_lineno = lineno

            except KeyboardInterrupt:
                pass

            return False


if __name__ == '__main__':

    def doit(cmd, args):
        proc = cmd.proc
        proc.current_command = ' '.join(args)
        cmd.run(args)


    from trepan.processor.command import mock as Mmock
    from trepan.processor.cmdproc import CommandProcessor
    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    cmdproc.frame = sys._getframe()
    cmdproc.setup()
    lcmd = ListCommand(cmdproc)
    print('--------------------')

    def foo():
        return 'bar'


    doit(lcmd, ['list', '40,', '60'])