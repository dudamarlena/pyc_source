# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/quit.py
# Compiled at: 2018-10-27 14:00:27
import os, threading
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan import exception as Mexcept
try:
    import ctypes

    def ctype_async_raise(thread_obj, exception):
        found = False
        target_tid = 0
        for (tid, tobj) in threading._active.items():
            if tobj is thread_obj:
                found = True
                target_tid = tid
                break

        if not found:
            raise ValueError('Invalid thread object')
        ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, ctypes.py_object(exception))
        if ret == 0:
            raise Mexcept.DebuggerQuit
        elif ret > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, 0)
            raise SystemError('PyThreadState_SetAsyncExc failed')


except ImportError:

    def ctype_async_raise(thread_obj, exception):
        pass


class QuitCommand(Mbase_cmd.DebuggerCommand):
    """**quit** [**unconditionally**]

Gently terminate the debugged program.

The program being debugged is aborted via a *DebuggerQuit*
exception.

When the debugger from the outside (e.g. via a `trepan` command), the
debugged program is contained inside a try block which handles the
*DebuggerQuit* exception.  However if you called the debugger was
started in the middle of a program, there might not be such an
exception handler; the debugged program still terminates but generally
with a traceback showing that exception.

If the debugged program is threaded, we raise an exception in each of
the threads ending with our own. However this might not quit the
program.

See also:
---------

See `exit` or `kill` for more forceful termination commands.

`run` and `restart` are other ways to restart the debugged program.
"""
    __module__ = __name__
    aliases = ('q', 'quit!')
    category = 'running'
    min_args = 0
    max_args = 0
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Terminate the program - gently'

    def nothread_quit(self, arg):
        """ quit command when there's just one thread. """
        self.debugger.core.stop()
        self.debugger.core.execution_status = 'Quit command'
        raise Mexcept.DebuggerQuit

    def threaded_quit(self, arg):
        """ quit command when several threads are involved. """
        threading_list = threading.enumerate()
        mythread = threading.currentThread()
        for t in threading_list:
            if t != mythread:
                ctype_async_raise(t, Mexcept.DebuggerQuit)

        raise Mexcept.DebuggerQuit

    def run(self, args):
        confirmed = False
        if len(args) <= 1:
            if '!' != args[0][(-1)]:
                confirmed = self.confirm('Really quit', False)
            else:
                confirmed = True
        if confirmed:
            threading_list = threading.enumerate()
            if (len(threading_list) == 1 or self.debugger.from_ipython) and threading.currentThread().getName() == 'MainThread':
                return self.nothread_quit(args)
            else:
                return self.threaded_quit(args)


if __name__ == '__main__':
    from trepan.processor.command import mock
    (d, cp) = mock.dbg_setup()
    command = QuitCommand(cp)
    try:
        command.run(['quit'])
    except Mexcept.DebuggerQuit:
        print "A got 'quit' a exception. Ok, be that way - I'm going home."
    else:

        class MyThread(threading.Thread):
            __module__ = __name__

            def run(self):
                command.run(['quit'])


        t = MyThread()
        t.start()
        t.join()