# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/python.py
# Compiled at: 2013-03-18 19:30:52
import code, os, sys
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')
Mmisc = import_relative('misc', '...', 'pydbgr')

class PythonCommand(Mbase_cmd.DebuggerCommand):
    """**python** [**-d**]

Run Python as a command subshell. The *sys.ps1* prompt will be set to
`Pydbgr >>> `.

If *-d* is passed, you can access debugger state via local variable *debugger*.

To issue a debugger command use function *dbgr()*. For example:

  dbgr('info program')
"""
    __module__ = __name__
    aliases = ('py', )
    category = 'support'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Run Python as a command subshell'

    def dbgr(self, string):
        """Invoke a debugger command from inside a python shell called inside
        the debugger. 
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

        banner_tmpl = 'Pydbgr python shell%s\nUse dbgr(*string*) to issue debugger command: *string*'
        debug = len(args) > 1 and args[1] == '-d'
        if debug:
            banner_tmpl += "\nVariable 'debugger' contains a pydbgr" + 'debugger object.'
        my_locals = {}
        my_globals = None
        if self.proc.curframe:
            my_globals = self.proc.curframe.f_globals
            if self.proc.curframe.f_locals:
                my_locals = self.proc.curframe.f_locals
        if debug:
            my_locals['debugger'] = self.debugger
        my_locals['dbgr'] = self.dbgr
        sys.ps1 = 'Pydbgr >>> '
        if len(my_locals):
            interact(banner=banner_tmpl % ' with locals', my_locals=my_locals, my_globals=my_globals)
        else:
            interact(banner=banner_tmpl % '')
        if have_line_edit:
            pass
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
    console = code.InteractiveConsole(my_locals, filename='<pydbgr>')
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
        exec (
         code_obj, obj.locals, obj.globals)
    except SystemExit:
        raise
    except:
        obj.showtraceback()
    else:
        if code.softspace(sys.stdout, 0):
            print ()


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = PythonCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    if len(sys.argv) > 1:
        print 'Type Python commands and exit to quit.'
        print sys.argv[1]
        if sys.argv[1] == '-d':
            print command.run(['python', '-d'])
        else:
            print command.run(['python'])