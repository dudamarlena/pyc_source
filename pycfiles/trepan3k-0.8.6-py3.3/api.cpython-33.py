# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/api.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 9380 bytes
"""Some singleton debugger methods that can be called without first
creating a debugger object -- these methods will create a debugger object,
if necessary, first.
"""
import sys
from trepan import debugger as Mdebugger, post_mortem as Mpost_mortem

def debugger_on_post_mortem():
    """Call debugger on an exeception that terminates a program"""
    sys.excepthook = Mpost_mortem.post_mortem_excepthook


def run_eval(expression, debug_opts=None, start_opts=None, globals_=None, locals_=None, tb_fn=None):
    """Evaluate the expression (given as a string) under debugger
    control starting with the statement subsequent to the place that
    this appears in your program.

    This is a wrapper to Debugger.run_eval(), so see that.

    When run_eval() returns, it returns the value of the expression.
    Otherwise this function is similar to run().
    """
    dbg = Mdebugger.Trepan(opts=debug_opts)
    try:
        try:
            return dbg.run_eval(expression, start_opts=start_opts, globals_=globals_, locals_=locals_)
        except:
            dbg.core.trace_hook_suspend = True
            if start_opts:
                if 'tb_fn' in start_opts:
                    tb_fn = start_opts['tb_fn']
            Mpost_mortem.uncaught_exception(dbg, tb_fn)

    finally:
        dbg.core.trace_hook_suspend = False


def run_call(func, debug_opts=None, start_opts=None, *args, **kwds):
    """Call the function (a function or method object, not a string)
    with the given arguments starting with the statement subsequent to
    the place that this appears in your program.

    When run_call() returns, it returns whatever the function call
    returned.  The debugger prompt appears as soon as the function is
    entered."""
    dbg = Mdebugger.Trepan(opts=debug_opts)
    try:
        return dbg.run_call(func, start_opts, *args, **kwds)
    except:
        Mpost_mortem.uncaught_exception(dbg)


def run_exec(statement, debug_opts=None, start_opts=None, globals_=None, locals_=None):
    """Execute the statement (given as a string) under debugger
    control starting with the statement subsequent to the place that
    this run_call appears in your program.

    This is a wrapper to Debugger.run_exec(), so see that.

    The debugger prompt appears before any code is executed;
    you can set breakpoints and type 'continue', or you can step
    through the statement using 'step' or 'next'

    The optional globals_ and locals_ arguments specify the environment
    in which the code is executed; by default the dictionary of the
    module __main__ is used."""
    dbg = Mdebugger.Trepan(opts=debug_opts)
    try:
        return dbg.run_exec(statement, start_opts=start_opts, globals_=globals_, locals_=locals_)
    except:
        Mpost_mortem.uncaught_exception(dbg)


def debug(dbg_opts=None, start_opts=None, post_mortem=True, step_ignore=1, level=0):
    """
Enter the debugger.

Parameters
----------

level : how many stack frames go back. Usually it will be
the default 0. But sometimes though there may be calls in setup to the debugger
that you may want to skip.

step_ignore : how many line events to ignore after the
debug() call. 0 means don't even wait for the debug() call to finish.

param dbg_opts : is an optional "options" dictionary that gets fed
trepan.Debugger(); `start_opts' are the optional "options"
dictionary that gets fed to trepan.Debugger.core.start().

Use like this:

.. code-block:: python

    ... # Possibly some Python code
    import trepan.api # Needed only once
    ... # Possibly some more Python code
    trepan.api.debug() # You can wrap inside conditional logic too
    pass  # Stop will be here.
    # Below is code you want to use the debugger to do things.
    ....  # more Python code
    # If you get to a place in the program where you aren't going
    # want to debug any more, but want to remove debugger trace overhead:
    trepan.api.stop()

Parameter "level" specifies how many stack frames go back. Usually it will be
the default 0. But sometimes though there may be calls in setup to the debugger
that you may want to skip.

Parameter "step_ignore" specifies how many line events to ignore after the
debug() call. 0 means don't even wait for the debug() call to finish.

In situations where you want an immediate stop in the "debug" call
rather than the statement following it ("pass" above), add parameter
step_ignore=0 to debug() like this::

    import trepan.api  # Needed only once
    # ... as before
    trepan.api.debug(step_ignore=0)
    # ... as before

Module variable _debugger_obj_ from module trepan.debugger is used as
the debugger instance variable; it can be subsequently used to change
settings or alter behavior. It should be of type Debugger (found in
module trepan). If not, it will get changed to that type::

   $ python
   >>> from trepan.debugger import debugger_obj
   >>> type(debugger_obj)
   <type 'NoneType'>
   >>> import trepan.api
   >>> trepan.api.debug()
   ...
   (Trepan) c
   >>> from trepan.debugger import debugger_obj
   >>> debugger_obj
   <trepan.debugger.Debugger instance at 0x7fbcacd514d0>
   >>>

If however you want your own separate debugger instance, you can
create it from the debugger _class Debugger()_ from module
trepan.debugger::

  $ python
  >>> from trepan.debugger import Debugger
  >>> dbgr = Debugger()  # Add options as desired
  >>> dbgr
  <trepan.debugger.Debugger instance at 0x2e25320>

`dbg_opts' is an optional "options" dictionary that gets fed
trepan.Debugger(); `start_opts' are the optional "options"
dictionary that gets fed to trepan.Debugger.core.start().
"""
    if not isinstance(Mdebugger.debugger_obj, Mdebugger.Trepan):
        Mdebugger.debugger_obj = Mdebugger.Trepan(dbg_opts)
        Mdebugger.debugger_obj.core.add_ignore(debug, stop)
    core = Mdebugger.debugger_obj.core
    frame = sys._getframe(0 + level)
    core.set_next(frame)
    if start_opts:
        if 'startup-profile' in start_opts and start_opts['startup-profile']:
            dbg_initfiles = start_opts['startup-profile']
            from trepan import options
            options.add_startup_file(dbg_initfiles)
            for init_cmdfile in dbg_initfiles:
                core.processor.queue_startfile(init_cmdfile)

    if not core.is_started():
        core.start(start_opts)
    if post_mortem:
        debugger_on_post_mortem()
    if 0 == step_ignore:
        frame = sys._getframe(1 + level)
        core.stop_reason = 'at a debug() call'
        old_trace_hook_suspend = core.trace_hook_suspend
        core.trace_hook_suspend = True
        core.processor.event_processor(frame, 'line', None)
        core.trace_hook_suspend = old_trace_hook_suspend
    else:
        core.step_ignore = step_ignore - 1
    return


def stop(opts=None):
    if isinstance(Mdebugger.Trepan, Mdebugger.debugger_obj):
        return Mdebugger.debugger_obj.stop(opts)
    else:
        return