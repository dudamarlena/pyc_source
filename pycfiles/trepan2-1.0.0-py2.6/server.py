# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/server.py
# Compiled at: 2016-05-03 20:16:10
import os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete, file as Mfile
from trepan.interfaces import server as Mserver
from trepan import debugger as Mdebugger

class ServerCommand(Mbase_cmd.DebuggerCommand):
    """**server** [**-v**][**-Y**|**-N**][**-c**] *file*

Read debugger commands from a file named *file*.  Optional *-v* switch
(before the filename) causes each command in *file* to be echoed as it
is executed.  Option *-Y* sets the default value in any confirmation
command to be "yes" and *-N* sets the default value to "no".

Note that the command startup file `.trepanc` is read automatically
via a *source* command the debugger is started.

An error in any command terminates execution of the command file
unless option `-c` is given."""
    category = 'support'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Read and run debugger commands from a file'

    def run(self, args):
        connection_opts = {'IO': 'TCP', 'PORT': int(args[1])}
        server_intf = Mserver.ServerInterface(connection_opts=connection_opts)
        self.errmsg("Going into server mode on port '%s'" % args[1])
        self.debugger.intf.append(server_intf)
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    (d, cp) = Mmock.dbg_setup()
    command = ServerCommand(cp)
    if len(sys.argv) > 1:
        command.run([sys.argv[1]])