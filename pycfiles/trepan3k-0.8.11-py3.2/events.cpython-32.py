# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/events.py
# Compiled at: 2015-06-06 21:00:50
import tracer
from trepan.processor.command import base_subcmd as Mbase_subcmd

class SetEvents(Mbase_subcmd.DebuggerSubcommand):
    """**set events** [*event* ...]

Sets the events that the debugger will stop on. Event names are:
`c_call`, `c_exception`, `c_return`, `call`, `exception`, `line`,
or `return`.

`all` can be used as an abbreviation for listing all event names.

Changing trace event filters works independently of turning on or off
tracing-event printing.

Examples:
---------

  set events line        # Set trace filter for line events only.
  set events call return # Trace calls and returns only
  set events all         # Set trace filter to all events.

See also:
---------

`set trace`, `show trace`, and `show events`. `help step` lists event names.
    """
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