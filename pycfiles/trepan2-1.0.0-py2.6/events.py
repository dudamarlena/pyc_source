# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/events.py
# Compiled at: 2015-02-17 12:15:19
import columnize
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowEvents(Mbase_subcmd.DebuggerSubcommand):
    """**show events**

Show the kinds of events the debugger will stop on.

See also:
---------

`set events`. `help step` lists of event names.
"""
    min_abbrev = 2
    short_help = 'Show the kinds of events the debugger will stop on'

    def run(self, args):
        events = list(self.debugger.settings['printset'])
        if events != []:
            events.sort()
            self.section('Trace events we may stop on:')
            self.msg(columnize.columnize(events, lineprefix='    '))
        else:
            self.msg('No events trapped.')
            return


if __name__ == '__main__':
    from trepan.processor.command import mock, show as Mshow
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    (d, cp) = mock.dbg_setup(d)
    i = Mshow.ShowCommand(cp)
    sub = ShowEvents(i)
    sub.run([])