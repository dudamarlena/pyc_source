# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/ipython.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 6704 bytes
import code, os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from traitlets.config.loader import Config

class IPythonCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**ipython** [**-d**]\n\nRun IPython as a command subshell.\n\nIf *-d* is passed, you can access debugger state via local variable *debugger*.\n\nTo issue a debugger command use function *dbgr()*. For example:\n\n  dbgr('info program')\n\nSee also:\n---------\n\n`python`, `bpython`\n"
    category = 'support'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Run IPython as a command subshell'

    def dbgr(self, string):
        """Invoke a debugger command from inside a IPython shell called
        inside the debugger.
        """
        self.proc.cmd_queue.append(string)
        self.proc.process_command()

    def run(self, args):
        have_line_edit = self.debugger.intf[(-1)].input.line_edit
        if have_line_edit:
            try:
                self.proc.write_history_file()
            except IOError:
                pass

        cfg = Config()
        banner_tmpl = 'IPython trepan2 shell%s\n\nUse dbgr(*string*) to issue non-continuing debugger command: *string*'
        debug = len(args) > 1 and args[1] == '-d'
        if debug:
            banner_tmpl += "\nVariable 'debugger' contains a trepan debugger object."
        try:
            from IPython.terminal.embed import InteractiveShellEmbed
        except ImportError:
            from IPython.frontend.terminal.embed import InteractiveShellEmbed

        my_locals = {}
        my_globals = None
        if self.proc.curframe:
            my_globals = self.proc.curframe.f_globals
            if self.proc.curframe.f_locals:
                my_locals = self.proc.curframe.f_locals
        if debug:
            my_locals['debugger'] = self.debugger
        my_locals['dbgr'] = self.dbgr
        cfg.TerminalInteractiveShell.confirm_exit = False
        if len(my_locals):
            banner = banner_tmpl % ' with locals'
        else:
            banner = banner_tmpl % ''
        InteractiveShellEmbed(config=cfg, banner1=banner, user_ns=my_locals, module=my_globals, exit_msg='IPython exiting to trepan3k...')()
        if hasattr(self.proc.intf[(-1)], 'complete'):
            try:
                from readline import set_completer, parse_and_bind
                parse_and_bind('tab: complete')
                set_completer(self.proc.intf[(-1)].complete)
            except ImportError:
                pass

        if have_line_edit:
            self.proc.read_history_file()
        return


def interact(banner=None, readfunc=None, my_locals=None, my_globals=None):
    """Almost a copy of code.interact
    Closely emulate the interactive Python interpreter.

    This is a backwards compatible interface to the InteractiveConsole
    class.  When readfunc is not specified, it attempts to import the
    readline module to enable GNU readline if it is available.

    Arguments (all optional, all default to None):

    banner -- passed to InteractiveConsole.interact()
    readfunc -- if not None, replaces InteractiveConsole.raw_input()
    local -- passed to InteractiveInterpreter.__init__()

    """
    console = code.InteractiveConsole(my_locals, filename='<trepan>')
    console.runcode = lambda code_obj: runcode(console, code_obj)
    setattr(console, 'globals', my_globals)
    if readfunc is not None:
        console.raw_input = readfunc
    else:
        try:
            import readline
        except ImportError:
            pass

    console.interact(banner)
    return


def runcode(obj, code_obj):
    """Execute a code object.

    When an exception occurs, self.showtraceback() is called to
    display a traceback.  All exceptions are caught except
    SystemExit, which is reraised.

    A note about KeyboardInterrupt: this exception may occur
    elsewhere in this code, and may not always be caught.  The
    caller should be prepared to deal with it.

    """
    try:
        exec(code_obj, obj.locals, obj.globals)
    except SystemExit:
        raise
    except:
        obj.showtraceback()
    else:
        if code.softspace(sys.stdout, 0):
            print()


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    command = IPythonCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    if len(sys.argv) > 1:
        print('Type Python commands and exit to quit.')
        print(sys.argv[1])
        if sys.argv[1] == '-d':
            print(command.run(['python', '-d']))
        else:
            print(command.run(['python']))