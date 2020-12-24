# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/events.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2568 bytes
import tracer
from trepan.processor.command import base_subcmd as Mbase_subcmd

class SetEvents(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = '**set events** [*event* ...]\n\nSets the events that the debugger will stop on. Event names are:\n`c_call`, `c_exception`, `c_return`, `call`, `exception`, `line`,\nor `return`.\n\n`all` can be used as an abbreviation for listing all event names.\n\nChanging trace event filters works independently of turning on or off\ntracing-event printing.\n\nExamples:\n---------\n\n  set events line        # Set trace filter for line events only.\n  set events call return # Trace calls and returns only\n  set events all         # Set trace filter to all events.\n\nSee also:\n---------\n\n`set trace`, `show trace`, and `show events`. `help step` lists event names.\n    '
    in_list = True
    min_abbrev = len('ev')
    short_help = 'Set execution-tracing event set'

    def run(self, args):
        valid_args = tracer.ALL_EVENT_NAMES + ('all', )
        eventset = []
        for arg in args:
            if arg not in valid_args:
                self.errmsg('set events: Invalid argument %s ignored.' % arg)
                continue
            if arg in tracer.ALL_EVENTS:
                eventset += [arg]
            elif 'all' == arg:
                eventset += tracer.ALL_EVENTS
                continue

        if [] != eventset:
            self.debugger.settings['printset'] = frozenset(eventset)


if __name__ == '__main__':
    from trepan.processor.command import mock, set as Mset
    d, cp = mock.dbg_setup()
    s = Mset.SetCommand(cp)
    sub = SetEvents(s)
    sub.name = 'events'
    for args in (['line'], ['bogus'],
     [
      'call', 'return']):
        sub.run(args)
        print(d.settings['printset'])