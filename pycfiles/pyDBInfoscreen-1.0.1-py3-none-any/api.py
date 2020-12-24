# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/api.py
# Compiled at: 2013-03-11 19:39:05
__doc__ = 'Some singleton debugger methods that can be called without first\ncreating a debugger object -- these methods will create a debugger object, \nif necessary, first.\n'
import sys
from import_relative import import_relative
Mdebugger = import_relative('debugger', top_name='pydbgr')
Mpost_mortem = import_relative('post_mortem', top_name='pydbgr')

def debugger_on_post_mortem():
    """Call debugger on an exeception that terminates a program"""
    sys.excepthook = Mpost_mortem.post_mortem_excepthook


def run_eval(expression, debug_opts=None, start_opts=None, globals_=None, locals_=None):
    """Evaluate the expression (given as a string) under debugger
    control starting with the statement subsequent to the place that
    this appears in your program.

    This is a wrapper to Debugger.run_eval(), so see that.

    When run_eval() returns, it returns the value of the expression.
    Otherwise this function is similar to run()."""
    dbg = Mdebugger.Debugger(opts=debug_opts)
    try:
        return dbg.run_eval(expression, start_opts=start_opts, globals_=globals_, locals_=locals_)
    except:
        Mpost_mortem.uncaught_exception(dbg)


def run_call(func, debug_opts=None, start_opts=None, *args, **kwds):
    """Call the function (a function or method object, not a string)
    with the given arguments starting with the statement subsequent to
    the place that this appears in your program.

    When run_call() returns, it returns whatever the function call
    returned.  The debugger prompt appears as soon as the function is
    entered."""
    dbg = Mdebugger.Debugger(opts=debug_opts)
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
    dbg = Mdebugger.Debugger(opts=debug_opts)
    try:
        return dbg.run_exec(statement, start_opts=start_opts, globals_=globals_, locals_=locals_)
    except:
        Mpost_mortem.uncaught_exception(dbg)


def debug(dbg_opts=None, start_opts=None, post_mortem=True, step_ignore=1):
    """ 
Enter the debugger. Use like this:

    ... # Possibly some Python code
    import pydbgr.api # Needed only once
    ... # Possibly some more Python code
    pydbgr.api.debug() # You can wrap inside conditional logic too
    pass  # Stop will be here.
    # Below is code you want to use the debugger to do things.
    ....  # more Python code
    # If you get to a place in the program where you aren't going 
    # want to debug any more, but want to remove debugger trace overhead:
    pydbgr.api.stop() 

In situations where you want an immediate stop in the "debug" call
rather than the statement following it ("pass" above), add parameter
step_ignore=0 to debug() like this:

    import pydbgr.api  # Needed only once
    # ... as before
    pydbgr.api.debug(step_ignore=0)
    # ... as before

Module variable debugger_obj from module pydbgr.debugger is used as
the debugger instance variable; it can be subsequenly used to change
settings or alter behavior. It should be of type Debugger (found in
module pydbgr). If not, it will get changed to that type.

   Example:
   $ python
   >>> from pydbgr.debugger import debugger_obj
   >>> type(debugger_obj)
   <type 'NoneType'>
   >>>  import pydbgr.api 
   >>>  pydbgr.api.debug()
   ...
   (Pydbgr) c
   >>> from pydbgr.debugger import debugger_obj
   >>> debugger_obj
   <pydbgr.debugger.Debugger instance at 0x7fbcacd514d0>
   >>>

If however you want your own separate debugger instance, you can
create it from the debugger class Debugger() from module
pydbgr.debugger.

Example:
  $ python
  >>> from pydbgr.debugger import Debugger
  >>> dbgr = Debugger()  # Add options as desired
  >>> dbgr
  <pydbgr.debugger.Debugger instance at 0x2e25320>

`dbg_opts' is an optional "options" dictionary that gets fed
pydbgr.Debugger(); `start_opts' are the optional "options"
dictionary that gets fed to pydbgr.Debugger.core.start().

Parameter "step_ignore" specifies how many line events to ignore after the
debug() call. 0 means don't even wait for the debug() call to finish.
"""
    if Mdebugger.Debugger != type(Mdebugger.debugger_obj):
        Mdebugger.debugger_obj = Mdebugger.Debugger(dbg_opts)
        Mdebugger.debugger_obj.core.add_ignore(debug, stop)
    core = Mdebugger.debugger_obj.core
    frame = sys._getframe(0)
    core.set_next(frame)
    if not core.is_started():
        core.start(start_opts)
    if post_mortem:
        debugger_on_post_mortem()
    if 0 == step_ignore:
        frame = sys._getframe(1)
        core.stop_reason = 'at a debug() call'
        old_trace_hook_suspend = core.trace_hook_suspend
        core.trace_hook_suspend = True
        core.processor.event_processor(frame, 'line', None)
        core.trace_hook_suspend = old_trace_hook_suspend
    else:
        core.step_ignore = step_ignore - 1
    return


def stop(opts=None):
    if Mdebugger.Debugger == type(Mdebugger.debugger_obj):
        return Mdebugger.debugger_obj.stop(opts)
    return


if __name__ == '__main__':
    import sys, tracer

    def foo(n):
        y = n
        for i in range(n):
            print i

        return y


    Mdefault = import_relative('default', 'lib', 'pydbgr')
    settings = dict(Mdefault.DEBUGGER_SETTINGS)
    settings.update({'trace': True, 'printset': tracer.ALL_EVENTS})
    debug_opts = {'step_ignore': -1, 'settings': settings}
    print 'Issuing: run_eval("1+2")'
    print run_eval('1+2', debug_opts=debug_opts)
    print 'Issuing: run_exec("x=1; y=2")'
    run_exec('x=1; y=2', debug_opts=debug_opts)
    print 'Issuing: run_call(foo, debug_opts, None, 2)'
    run_call(foo, debug_opts, None, 2)