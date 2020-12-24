# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/width.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 939 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.processor import cmdfns as Mcmdfns

class SetWidth(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = '**set width** *number*\n\nSet the number of characters the debugger thinks are in a line.\n\nSee also:\n--------\n\n`show width`\n'
    in_list = True
    min_abbrev = len('wid')
    short_help = 'Set the width of the terminal'

    def run(self, args):
        Mcmdfns.run_set_int(self, ' '.join(args), "The 'width' command requires a line width", 0, None)
        return


if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    sub = Mhelper.demo_run(SetWidth)
    d = sub.proc.debugger
    sub.run(['100'])
    print(d.settings['width'])