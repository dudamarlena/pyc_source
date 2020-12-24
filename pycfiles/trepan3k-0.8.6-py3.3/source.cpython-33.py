# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/source.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3100 bytes
import os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete, file as Mfile
from trepan.interfaces import script as Mscript
from trepan import debugger as Mdebugger

class SourceCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**source** [**-v**][**-Y**|**-N**][**-c**] *file*\n\nRead debugger commands from a file named *file*.  Optional *-v* switch\n(before the filename) causes each command in *file* to be echoed as it\nis executed.  Option *-Y* sets the default value in any confirmation\ncommand to be "yes" and *-N* sets the default value to "no".\n\nNote that the command startup file `.trepan3krc` is read automatically\nvia a *source* command the debugger is started.\n\nAn error in any command terminates execution of the command file\nunless option `-c` is given.'
    category = 'support'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Read and run debugger commands from a file'

    def complete(self, prefix):
        opts = [
         '-v', '-Y', '-N', '-c']
        return Mcomplete.complete_token(opts, prefix)

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
                continue

        filename = args[(-1)]
        expanded_file = os.path.expanduser(filename)
        if not Mfile.readable(expanded_file):
            self.errmsg("Debugger command file '%s' is not a readable file" % filename)
            return False
        script_intf = Mscript.ScriptInterface(expanded_file, opts=opts, out=self.debugger.intf[(-1)].output)
        self.debugger.intf.append(script_intf)
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    d, cp = Mmock.dbg_setup()
    command = SourceCommand(cp)
    if len(sys.argv) > 1:
        command.run([sys.argv[1]])