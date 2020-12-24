# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/post_mortem.py
# Compiled at: 2017-10-28 10:37:24
import inspect, os, sys, re, traceback
from trepan import debugger as Mdebugger
from trepan.exception import DebuggerQuit, DebuggerRestart

def get_last_or_frame_exception():
    """Intended to be used going into post mortem routines.  If
    sys.last_traceback is set, we will return that and assume that
    this is what post-mortem will want. If sys.last_traceback has not
    been set, then perhaps we *about* to raise an error and are
    fielding an exception. So assume that sys.exc_info()[2]
    is where we want to look."""
    try:
        if inspect.istraceback(sys.last_traceback):
            return (
             sys.last_type, sys.last_value, sys.last_traceback)
    except AttributeError:
        pass

    return sys.exc_info()


def pm(frameno=1, dbg=None):
    """Set up post-mortem debugging using the last traceback.  But if
    there is no traceback, we'll assume that sys.exc_info() contains
    what we want and frameno is the index location of where we want
    to start.

    'dbg', is an optional trepan.Debugger object.
    """
    post_mortem(get_last_or_frame_exception(), frameno, dbg=dbg)


def post_mortem_excepthook(exc_type, exc_value, exc_tb, tb_fn=None):
    if str(exc_type) == str(DebuggerQuit):
        return
    try:
        if str(exc_type) == str(DebuggerRestart):
            if exc_value and exc_value.sys_argv and len(exc_value.sys_argv) > 0:
                print 'No restart handler - trying restart via execv(%s)' % repr(exc_value.sys_argv)
                os.execvp(exc_value.sys_argv[0], exc_value.sys_argv)
            else:
                print 'No restart handler, no params registered'
                print 'Entering post-mortem debugger...'
        else:
            if tb_fn:
                tb_fn(exc_type, exc_value, exc_tb)
            else:
                traceback.print_exception(exc_type, exc_value, exc_tb)
            print 'Uncaught exception. Entering post-mortem debugger...'
        post_mortem((exc_type, exc_value, exc_tb))
        print 'Post-mortem debugger finished.'
    except:
        pass


def post_mortem(exc=None, frameno=1, dbg=None):
    """Enter debugger read loop after your program has crashed.

    exc is a triple like you get back from sys.exc_info.  If no exc
    parameter, is supplied, the values from sys.last_type,
    sys.last_value, sys.last_traceback are used. And if these don't
    exist either we'll assume that sys.exc_info() contains what we
    want and frameno is the index location of where we want to start.

    'frameno' specifies how many frames to ignore in the traceback.
    The default is 1, that is, we don't need to show the immediate
    call into post_mortem. If you have wrapper functions that call
    this one, you may want to increase frameno.
    """
    if dbg is None:
        if Mdebugger.debugger_obj is None:
            Mdebugger.debugger_obj = Mdebugger.Debugger()
        dbg = Mdebugger.debugger_obj
    re_bogus_file = re.compile('^<.+>$')
    if exc[0] is None:
        exc = get_last_or_frame_exception()
        if exc[0] is None:
            print "Can't find traceback for post_mortem in sys.last_traceback or sys.exec_info()"
            return
    (exc_type, exc_value, exc_tb) = exc
    dbg.core.execution_status = 'Terminated with unhandled exception %s' % exc_type
    if exc_tb is not None:
        while exc_tb.tb_next is not None:
            filename = exc_tb.tb_frame.f_code.co_filename
            if dbg.mainpyfile and 0 == len(dbg.mainpyfile) and not re_bogus_file.match(filename):
                dbg.mainpyfile = filename
            exc_tb = exc_tb.tb_next

        dbg.core.processor.curframe = exc_tb.tb_frame
    if 0 == len(dbg.program_sys_argv):
        dbg.program_sys_argv = list(sys.argv[1:])
        dbg.program_sys_argv[:0] = [dbg.mainpyfile]
    try:
        f = exc_tb.tb_frame
        if f and f.f_lineno != exc_tb.tb_lineno:
            f = f.f_back
        dbg.core.processor.event_processor(f, 'exception', exc, 'trepan2:pm')
    except DebuggerRestart:
        while True:
            sys.argv = list(dbg._program_sys_argv)
            dbg.msg('Restarting %s with arguments:\n\t%s' % (
             dbg.filename(dbg.mainpyfile),
             (' ').join(dbg._program_sys_argv[1:])))
            try:
                dbg.run_script(dbg.mainpyfile)
            except DebuggerRestart:
                pass

    except DebuggerQuit:
        pass

    return


def uncaught_exception(dbg, tb_fn=None):
    exc = sys.exc_info()
    (exc_type, exc_value, exc_tb) = exc
    if exc_type == DebuggerQuit:
        return
    else:
        if exc_type == DebuggerRestart:
            print 'restart not done yet - entering post mortem debugging'
        else:
            if exc_tb is None:
                print "You don't seem to have an exception traceback, yet."
                return
            if tb_fn:
                tb_fn(exc_type, exc_value, exc_tb)
            else:
                traceback.print_exception(exc_type, exc_value, exc_tb)
            print 'uncaught exception. entering post mortem debugging'
        dbg.core.execution_status = 'Terminated with unhandled exception %s' % exc_type
        dbg.core.processor.event_processor(exc_tb.tb_frame, 'exception', exc, 'trepan2:pm')
        print 'Post mortem debugger finished.'
        return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pm()