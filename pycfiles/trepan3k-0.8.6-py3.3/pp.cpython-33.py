# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/pp.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2114 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import pp as Mpp
from trepan.processor import complete as Mcomplete

class PrettyPrintCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**pp** *expression*\n\nPretty-print the value of the expression.\n\nSimple arrays are shown columnized horizontally. Other values are printed\nvia *pprint.pformat()*.\n\nSee also:\n---------\n\n`pr` and `examine` for commands which do more in the way of\nformatting.\n'
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Pretty print value of expression EXP'
    complete = Mcomplete.complete_identifier

    def run(self, args):
        arg = ' '.join(args[1:])
        val = self.proc.eval(arg)
        Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg)
        return False


if __name__ == '__main__':
    import inspect
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    cp.curframe = inspect.currentframe()
    command = PrettyPrintCommand(cp)
    me = list(range(10))
    command.run(['pp', 'me'])
    me = list(range(100))
    command.run(['pp', 'me'])
    import sys
    command.run(['pp', 'sys.modules.keys()'])
    me = 'fooled you'
    command.run(['pp', 'locals()'])