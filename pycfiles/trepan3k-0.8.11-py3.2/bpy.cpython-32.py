# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/bpy.py
# Compiled at: 2015-11-27 21:52:29
import code, os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
import bpython

class PythonCommand(Mbase_cmd.DebuggerCommand):
    """**bpython** [**-d**]

Run bpython as a command subshell. The *sys.ps1* prompt will be set to
`trepan2 >>> `.

If *-d* is passed, you can access debugger state via local variable *debugger*.

To issue a debugger command use function *dbgr()*. For example:

  dbgr('info program')
"""
    aliases = ('bpython', )
    category = 'support'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Run bpython as a command subshell'

    def dbgr(self, string):
        """Invoke a debugger command from inside a python shell called inside
        the debugger.
        """
        print('')
        self.proc.cmd_queue.append(string)
        self.proc.process_command()

    def run(self, args):
        try:
            from bpython.curtsies import main as main_bpython
        except ImportError:
            self.errmsg('bpython needs to be installed to run this command')
            return

        have_line_edit = self.debugger.intf[(-1)].input.line_edit
        if have_line_edit:
            try:
                self.proc.write_history_file()
            except IOError:
                pass

        banner_tmpl = 'trepan2 python shell%s\nUse dbgr(*string*) to issue debugger command: *string*'
        debug = len(args) > 1 and args[1] == '-d'
        if debug:
            banner_tmpl += "\nVariable 'debugger' contains a trepan" + 'debugger object.'
        my_locals = {}
        if self.proc.curframe:
            if self.proc.curframe.f_locals:
                my_locals = self.proc.curframe.f_locals
        if debug:
            my_locals['debugger'] = self.debugger
        my_locals['dbgr'] = self.dbgr
        if len(my_locals):
            banner = banner_tmpl % ' with locals'
        else:
            banner = banner_tmpl % ''
        sys.ps1 = 'trepan2 >>> '
        print(banner)
        try:
            main_bpython([], my_locals)
        except SystemExit:
            pass

        if hasattr(self.proc.intf[(-1)], 'complete'):
            try:
                from readline import set_completer, parse_and_bind
                parse_and_bind('tab: complete')
                set_completer(self.proc.intf[(-1)].complete)
            except ImportError:
                pass

        if have_line_edit:
            self.proc.read_history_file()