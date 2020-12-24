# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/source.py
# Compiled at: 2013-01-12 04:26:22
import os, sys
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mdebugger = import_relative('debugger', '...', 'pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')
Mscript = import_relative('script', '...interfaces', 'pydbgr')

class SourceCommand(Mbase_cmd.DebuggerCommand):
    """**source** [**-v**][**-Y**|**-N**][**-c**] *file*

Read debugger commands from a file named *file*.  Optional *-v* switch
(before the filename) causes each command in *file* to be echoed as it
is executed.  Option *-Y* sets the default value in any confirmation
command to be "yes" and *-N* sets the default value to "no".

Note that the command startup file `.pydbgrc` is read automatically
via a *source* command the debugger is started.

An error in any command terminates execution of the command file
unless option `-c` is given."""
    __module__ = __name__
    category = 'support'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Read and run debugger commands from a file'

    def run(self, args):
        parms = args[1:-1]
        opts = {}
        for arg in parms:
            if arg == '-v':
                opts['verbose'] = True
            elif arg == '-Y':
                opts['confirm_val'] = True
            elif arg == '-N':
                opts['confirm_val'] = False
            elif arg == '-c':
                opts['abort_on_error'] = False

        filename = args[(-1)]
        expanded_file = os.path.expanduser(filename)
        if not Mfile.readable(expanded_file):
            self.errmsg("Debugger command file '%s' is not a readable file" % filename)
            return False
        script_intf = Mscript.ScriptInterface(expanded_file, opts=opts, out=self.debugger.intf[(-1)].output)
        self.debugger.intf.append(script_intf)
        return False


if __name__ == '__main__':
    Mmock = import_relative('mock')
    (d, cp) = Mmock.dbg_setup()
    command = SourceCommand(cp)
    if len(sys.argv) > 1:
        command.run([sys.argv[1]])