# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/core.py
# Compiled at: 2020-01-29 15:49:53
"""
Core
"""
import sys, asyncore, signal, threading, time, traceback, warnings
from .task import TaskManager
from .debugging import bacpypes_debugging, ModuleLogger
_debug = 0
_log = ModuleLogger(globals())
running = False
taskManager = None
deferredFns = []
sleeptime = 0.0

@bacpypes_debugging
def stop(*args):
    """Call to stop running, may be called with a signum and frame
    parameter if called as a signal handler."""
    global running
    global taskManager
    if _debug:
        stop._debug('stop')
    if args:
        sys.stderr.write('===== TERM Signal, %s\n' % time.strftime('%d-%b-%Y %H:%M:%S'))
        sys.stderr.flush()
    running = False
    if taskManager and taskManager.trigger:
        if _debug:
            stop._debug('    - trigger')
        taskManager.trigger.set()


@bacpypes_debugging
def dump_stack(debug_handler):
    if _debug:
        dump_stack._debug('dump_stack %r', debug_handler)
    for filename, lineno, fn, _ in traceback.extract_stack()[:-1]:
        debug_handler('    %-20s  %s:%s', fn, filename.split('/')[(-1)], lineno)


@bacpypes_debugging
def print_stack(sig, frame):
    """Signal handler to print a stack trace and some interesting values."""
    global deferredFns
    global sleeptime
    if _debug:
        print_stack._debug('print_stack %r %r', sig, frame)
    sys.stderr.write('==== USR1 Signal, %s\n' % time.strftime('%d-%b-%Y %H:%M:%S'))
    sys.stderr.write('---------- globals\n')
    sys.stderr.write('    running: %r\n' % (running,))
    sys.stderr.write('    deferredFns: %r\n' % (deferredFns,))
    sys.stderr.write('    sleeptime: %r\n' % (sleeptime,))
    sys.stderr.write('---------- stack\n')
    traceback.print_stack(frame)
    flist = []
    f = frame
    while f.f_back:
        flist.append(f)
        f = f.f_back

    flist.reverse()
    for f in flist:
        sys.stderr.write('---------- frame: %s\n' % (f,))
        for k, v in f.f_locals.items():
            sys.stderr.write('    %s: %r\n' % (k, v))

    sys.stderr.flush()


SPIN = 1.0

@bacpypes_debugging
def run(spin=SPIN, sigterm=stop, sigusr1=print_stack):
    global deferredFns
    global running
    global taskManager
    if _debug:
        run._debug('run spin=%r sigterm=%r, sigusr1=%r', spin, sigterm, sigusr1)
    if isinstance(threading.current_thread(), threading._MainThread):
        if sigterm is not None and hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, sigterm)
        if sigusr1 is not None and hasattr(signal, 'SIGUSR1'):
            signal.signal(signal.SIGUSR1, sigusr1)
    else:
        if sigterm or sigusr1:
            warnings.warn('no signal handlers for child threads')
        taskManager = TaskManager()
        loopCount = 0
        running = True
        while running:
            loopCount += 1
            task, delta = taskManager.get_next_task()
            try:
                if task:
                    taskManager.process_task(task)
                if delta is None:
                    delta = spin
                if sleeptime and delta > sleeptime:
                    time.sleep(sleeptime)
                    delta -= sleeptime
                delta = min(delta, spin)
                if deferredFns:
                    delta = min(delta, 0.001)
                asyncore.loop(timeout=delta, count=1)
                while deferredFns:
                    fnlist = deferredFns
                    deferredFns = []
                    for fn, args, kwargs in fnlist:
                        fn(*args, **kwargs)

                    del fnlist

            except KeyboardInterrupt:
                if _debug:
                    run._info('keyboard interrupt')
                running = False
            except Exception as err:
                run._exception('an error has occurred: %s', err)

    running = False
    return


@bacpypes_debugging
def run_once():
    """
    Make a pass through the scheduled tasks and deferred functions just
    like the run() function but without the asyncore call (so there is no
    socket IO actviity) and the timers.
    """
    global deferredFns
    global taskManager
    if _debug:
        run_once._debug('run_once')
    taskManager = TaskManager()
    try:
        delta = 0.0
        while delta == 0.0:
            task, delta = taskManager.get_next_task()
            if _debug:
                run_once._debug('    - task, delta: %r, %r', task, delta)
            if task:
                taskManager.process_task(task)
            while deferredFns:
                fnlist = deferredFns
                deferredFns = []
                for fn, args, kwargs in fnlist:
                    if _debug:
                        run_once._debug('    - call: %r %r %r', fn, args, kwargs)
                    fn(*args, **kwargs)

                del fnlist

    except KeyboardInterrupt:
        if _debug:
            run_once._info('keyboard interrupt')
    except Exception as err:
        run_once._exception('an error has occurred: %s', err)


@bacpypes_debugging
def deferred(fn, *args, **kwargs):
    if _debug:
        deferred._debug('deferred %r %r %r', fn, args, kwargs)
    deferredFns.append((fn, args, kwargs))
    if taskManager and taskManager.trigger:
        if _debug:
            deferred._debug('    - trigger')
        taskManager.trigger.set()


@bacpypes_debugging
def enable_sleeping(stime=0.001):
    global sleeptime
    if _debug:
        enable_sleeping._debug('enable_sleeping %r', stime)
    sleeptime = stime