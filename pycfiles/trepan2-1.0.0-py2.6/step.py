# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/step.py
# Compiled at: 2015-06-02 07:34:10
import os, tracer
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import cmdfns as Mcmdfns

class StepCommand(Mbase_cmd.DebuggerCommand):
    """**step**[**+**|**-**|**<**|**>**|**!**] [*event*...] [*count*]

Execute the current line, stopping at the next event.

With an integer argument, step that many times.

*event* is list of an event name which is one of: `call`,
`return`, `line`, `exception` `c-call`, `c-return` or `c-exception`.
If specified, only those stepping events will be considered. If no
list of event names is given, then any event triggers a stop when the
count is 0.

There is however another way to specify a *single* event, by
suffixing one of the symbols `<`, `>`, or `!` after the command or on
an alias of that.  A suffix of `+` on a command or an alias forces a
move to another line, while a suffix of `-` disables this requirement.
A suffix of `>` will continue until the next call. (`finish` will run
run until the return for that call.)

If no suffix is given, the debugger setting `different-line`
determines this behavior.

Examples:
---------

  step        # step 1 event, *any* event
  step 1      # same as above
  step 5/5+0  # same as above
  step line   # step only line events
  step call   # step only call events
  step>       # same as above
  step call line # Step line *and* call events

Related and similar is the `next` command.

See also:
---------

`next`, `skip`, `jump` (there's no `hop` yet), `continue`, `return` and
`finish` for other ways to progress execution.
"""
    aliases = ('step+', 'step-', 'step>', 'step<', 'step!', 's', 's+', 's-', 's<',
               's>', 's!')
    category = 'running'
    min_args = 0
    max_args = None
    execution_set = ['Running']
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Step program (possibly entering called functions)'

    def run(self, args):
        step_events = []
        if args[0][(-1)] == '>':
            step_events = [
             'call']
        elif args[0][(-1)] == '<':
            step_events = [
             'return']
        elif args[0][(-1)] == '!':
            step_events = [
             'exception']
        if len(args) <= 1:
            self.proc.debugger.core.step_ignore = 0
        else:
            pos = 1
            while pos < len(args):
                arg = args[pos]
                if arg in tracer.ALL_EVENT_NAMES:
                    step_events.append(arg)
                else:
                    break
                pos += 1

            if pos == len(args) - 1:
                self.core.step_ignore = self.proc.get_int(args[pos], default=1, cmdname='step')
                if self.core.step_ignore is None:
                    return False
                self.core.step_ignore -= 1
            elif pos != len(args):
                self.errmsg('Invalid additional parameters %s' % (' ').join(args[pos]))
                return False
        if [] == step_events:
            self.core.step_events = None
        else:
            self.core.step_events = step_events
        self.core.different_line = Mcmdfns.want_different_line(args[0], self.settings['different'])
        self.core.stop_level = None
        self.core.last_frame = None
        self.core.stop_on_finish = False
        self.proc.continue_running = True
        return True


if __name__ == '__main__':
    from mock import MockDebugger
    d = MockDebugger()
    cmd = StepCommand(d.core.processor)
    for c in (['s', '5'],
     [
      'step', '1+2'],
     [
      's', 'foo']):
        d.core.step_ignore = 0
        cmd.proc.continue_running = False
        result = cmd.run(c)
        print 'Execute result: %s' % result
        print 'step_ignore %s' % repr(d.core.step_ignore)
        print 'continue_running: %s' % cmd.proc.continue_running

    for c in (['s'], ['step+'], ['s-'], ['s!'], ['s>'], ['s<']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print 'different line %s:' % c[0], cmd.core.different_line