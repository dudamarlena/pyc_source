# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/debugger.py
# Compiled at: 2020-04-27 23:16:57
"""Debugger class and top-level debugger functions.

This module contains the `Debugger' class and some top-level routines
for creating and invoking a debugger. Most of this module serves as:
  * a wrapper for `Debugger.core' routines,
  * a place to define `Debugger' exceptions, and
  * `Debugger' settings.

See also module `cli' which contains a command-line interface to debug
a Python script and `core' which contains the core debugging
start/stop and event-handling dispatcher and `client.py' which is a
user or client-side code for connecting to server'd debugged program.
"""
from trepan.exception import DebuggerQuit, DebuggerRestart
import trepan.lib.default as Mdefault, trepan.interfaces.user as Muser
from trepan.misc import option_set
import trepan.lib.sighandler as Msig, sys, types, tracer, tracefilter, pyficache
debugger_obj = None
try:
    from readline import get_line_buffer
except ImportError:

    def get_line_buffer():
        return


class Debugger():

    def run(self, cmd, start_opts=None, globals_=None, locals_=None):
        """ Run debugger on string `cmd' using builtin function eval
        and if that builtin exec.  Arguments `globals_' and `locals_'
        are the dictionaries to use for local and global variables. By
        default, the value of globals is globals(), the current global
        variables. If `locals_' is not given, it becomes a copy of
        `globals_'.

        Debugger.core.start settings are passed via optional
        dictionary `start_opts'. Overall debugger settings are in
        Debugger.settings which changed after an instance is created
        . Also see `run_eval' if what you want to run is an
        run_eval'able expression have that result returned and
        `run_call' if you want to debug function run_call.
        """
        if globals_ is None:
            globals_ = globals()
        if locals_ is None:
            locals_ = globals_
        if not isinstance(cmd, types.CodeType):
            self.eval_string = cmd
            cmd = cmd + '\n'
        retval = None
        self.core.start(start_opts)
        try:
            retval = eval(cmd, globals_, locals_)
        except SyntaxError:
            try:
                exec (
                 cmd, globals_, locals_)
            except DebuggerQuit:
                pass
            except DebuggerQuit:
                pass

        except DebuggerQuit:
            pass

        self.core.stop()
        return retval

    def run_exec(self, cmd, start_opts=None, globals_=None, locals_=None):
        """ Run debugger on string `cmd' which will executed via the
        builtin function exec. Arguments `globals_' and `locals_' are
        the dictionaries to use for local and global variables. By
        default, the value of globals is globals(), the current global
        variables. If `locals_' is not given, it becomes a copy of
        `globals_'.

        Debugger.core.start settings are passed via optional
        dictionary `start_opts'. Overall debugger settings are in
        Debugger.settings which changed after an instance is created
        . Also see `run_eval' if what you want to run is an
        run_eval'able expression have that result returned and
        `run_call' if you want to debug function run_call.
        """
        if globals_ is None:
            globals_ = globals()
        if locals_ is None:
            locals_ = globals_
        if not isinstance(cmd, types.CodeType):
            cmd = cmd + '\n'
        self.core.start(start_opts)
        try:
            exec (cmd, globals_, locals_)
        except DebuggerQuit:
            pass

        self.core.stop()
        return

    def run_call(self, func, start_opts=None, *args, **kwds):
        """ Run debugger on function call: `func(*args, **kwds)'

        See also `run_eval' if what you want to run is an eval'able
        expression have that result returned and `run' if you want to
        debug a statment via exec.
        """
        res = None
        self.core.start(opts=start_opts)
        try:
            res = func(*args, **kwds)
        except DebuggerQuit:
            pass

        self.core.stop()
        return res

    def run_eval(self, expr, start_opts=None, globals_=None, locals_=None):
        """ Run debugger on string `expr' which will executed via the
        built-in Python function: eval; `globals_' and `locals_' are
        the dictionaries to use for local and global variables. If
        `globals' is not given, __main__.__dict__ (the current global
        variables) is used. If `locals_' is not given, it becomes a
        copy of `globals_'.

        See also `run_call' if what you to debug a function call and
        `run' if you want to debug general Python statements.
        """
        if globals_ is None:
            globals_ = globals()
        if locals_ is None:
            locals_ = globals_
        if not isinstance(expr, types.CodeType):
            self.eval_string = expr
            expr = expr + '\n'
        retval = None
        self.core.start(start_opts)
        try:
            try:
                retval = eval(expr, globals_, locals_)
            except DebuggerQuit:
                pass

        finally:
            pyficache.remove_remap_file('<string>')
            self.core.stop()

        return retval

    def run_script(self, filename, start_opts=None, globals_=None, locals_=None):
        """ Run debugger on Python script `filename'. The script may
        inspect sys.argv for command arguments. `globals_' and
        `locals_' are the dictionaries to use for local and global
        variables. If `globals' is not given, globals() (the current
        global variables) is used. If `locals_' is not given, it
        becomes a copy of `globals_'.

        True is returned if the program terminated normally and False
        if the debugger initiated a quit or the program did not normally
        terminate.

        See also `run_call' if what you to debug a function call,
        `run_eval' if you want to debug an expression, and `run' if you
        want to debug general Python statements not inside a file.
        """
        self.mainpyfile = self.core.canonic(filename)
        if globals_ is None:
            import __main__
            globals_ = {'__name__': '__main__', '__file__': self.mainpyfile, '__builtins__': __builtins__}
        if locals_ is None:
            locals_ = globals_
        self.core.start(start_opts)
        retval = False
        self.core.execution_status = 'Running'
        try:
            exec (
             compile(open(self.mainpyfile).read(), self.mainpyfile, 'exec'), globals_, locals_)
            retval = True
        except SyntaxError:
            print sys.exc_info()[1]
            retval = False
        except IOError:
            print sys.exc_info()[1]
        except DebuggerQuit:
            retval = False
        except DebuggerRestart:
            self.core.execution_status = 'Restart requested'
            raise DebuggerRestart

        self.core.stop(options={'remove': True})
        return retval

    def restart_argv(self):
        """Return an array that would be execv-ed  to restart the program"""
        return self.orig_sys_argv or self.program_sys_argv

    DEFAULT_INIT_OPTS = {'ignore_filter': tracefilter.TraceFilter([
                       tracer.start, tracer.stop,
                       run_eval, run_call, run_eval, run_script]), 
       'orig_sys_argv': None, 
       'save_sys_argv': True, 
       'activate': False, 
       'interface': None, 
       'input': None, 
       'output': None, 
       'processor': None, 
       'settings': Mdefault.DEBUGGER_SETTINGS, 
       'start_opts': Mdefault.START_OPTS, 
       'step_ignore': 0, 
       'from_ipython': False}

    def __init__(self, opts=None):
        """Create a debugger object. But depending on the value of
        key 'start' inside hash 'opts', we may or may not initially
        start debugging.

        See also Debugger.start and Debugger.stop.
        """
        import trepan.lib.core as Mcore
        self.mainpyfile = None
        self.thread = None
        self.eval_string = None
        get_option = lambda key: option_set(opts, key, self.DEFAULT_INIT_OPTS)
        completer = lambda text, state: self.complete(text, state)
        for opt in ('settings', 'orig_sys_argv', 'from_ipython'):
            setattr(self, opt, get_option(opt))

        core_opts = {}
        for opt in ('ignore_filter', 'proc_opts', 'processor', 'step_ignore', 'processor'):
            core_opts[opt] = get_option(opt)

        interface_opts = {'complete': completer}
        interface = get_option('interface') or Muser.UserInterface(opts=interface_opts)
        self.intf = [interface]
        inp = get_option('input')
        if inp:
            self.intf[(-1)].input = inp
        out = get_option('output')
        if out:
            self.intf[(-1)].output = out
        self.core = Mcore.DebuggerCore(self, core_opts)
        self.core.add_ignore(self.core.stop)
        self.core.trace_hook_suspend = False
        if get_option('save_sys_argv'):
            self.program_sys_argv = list(sys.argv)
        else:
            self.program_sys_argv = None
        self.sigmgr = Msig.SignalManager(self)
        if get_option('activate'):
            self.core.start(get_option('start_opts'))
        return

    def complete(self, last_token, state):
        if hasattr(self.core.processor, 'completer'):
            str = get_line_buffer() or last_token
            results = self.core.processor.completer(str, state)
            return results[state]
        else:
            return [
             None]
            return


if __name__ == '__main__':

    def foo():
        y = 2
        for i in range(2):
            print '%d %d' % (i, y)

        return 3


    import debugger
    d = debugger.Debugger()
    d.settings['trace'] = True
    d.settings['printset'] = tracer.ALL_EVENTS
    d.core.step_ignore = -1
    print 'Issuing: run_eval("1+2")'
    print d.run_eval('1+2')
    print 'Issuing: run_exec("x=1; y=2")'
    d.run_exec('x=1; y=2')
    print 'Issuing: run("3*4")'
    print d.run('3*4')
    print 'Issuing: run("x=3; y=4")'
    d.run('x=3; y=4')
    print 'Issuing: run_call(foo)'
    d.run_call(foo)
    if len(sys.argv) > 1:
        while True:
            try:
                print 'started'
                d.core.step_ignore = 0
                d.core.start()
                x = 4
                x = foo()
                for i in range(2):
                    print '%d' % (i + 1) * 10

                d.core.stop()

                def square(x):
                    return x * x


                print 'calling: run_call(square,2)'
                d.run_call(square, 2)
            except DebuggerQuit:
                print "That's all Folks!..."
                break
            except DebuggerRestart:
                print 'Restarting...'