# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/exceptionHandling.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4149 bytes
"""This module installs a wrapper around sys.excepthook which allows multiple
new exception handlers to be registered. 

Optionally, the wrapper also stops exceptions from causing long-term storage 
of local stack frames. This has two major effects:
  - Unhandled exceptions will no longer cause memory leaks
    (If an exception occurs while a lot of data is present on the stack, 
    such as when loading large files, the data would ordinarily be kept
    until the next exception occurs. We would rather release this memory 
    as soon as possible.)
  - Some debuggers may have a hard time handling uncaught exceptions
 
The module also provides a callback mechanism allowing others to respond 
to exceptions.
"""
import sys, time, traceback
callbacks = []
clear_tracebacks = False

def register(fn):
    """
    Register a callable to be invoked when there is an unhandled exception.
    The callback will be passed the output of sys.exc_info(): (exception type, exception, traceback)
    Multiple callbacks will be invoked in the order they were registered.
    """
    global callbacks
    callbacks.append(fn)


def unregister(fn):
    """Unregister a previously registered callback."""
    callbacks.remove(fn)


def setTracebackClearing(clear=True):
    """
    Enable or disable traceback clearing.
    By default, clearing is disabled and Python will indefinitely store unhandled exception stack traces.
    This function is provided since Python's default behavior can cause unexpected retention of 
    large memory-consuming objects.
    """
    global clear_tracebacks
    clear_tracebacks = clear


class ExceptionHandler(object):

    def __call__(self, *args):
        global original_excepthook
        recursionLimit = sys.getrecursionlimit()
        try:
            sys.setrecursionlimit(recursionLimit + 100)
            try:
                print('===== %s =====' % str(time.strftime('%Y.%m.%d %H:%m:%S', time.localtime(time.time()))))
            except Exception:
                sys.stderr.write('Warning: stdout is broken! Falling back to stderr.\n')
                sys.stdout = sys.stderr

            ret = original_excepthook(*args)
            for cb in callbacks:
                try:
                    cb(*args)
                except Exception:
                    print('   --------------------------------------------------------------')
                    print('      Error occurred during exception callback %s' % str(cb))
                    print('   --------------------------------------------------------------')
                    (traceback.print_exception)(*sys.exc_info())

            if clear_tracebacks is True:
                sys.last_traceback = None
        finally:
            sys.setrecursionlimit(recursionLimit)

    def implements(self, interface=None):
        if interface is None:
            return [
             'ExceptionHandler']
        return interface == 'ExceptionHandler'


if not (hasattr(sys.excepthook, 'implements') and sys.excepthook.implements('ExceptionHandler')):
    original_excepthook = sys.excepthook
    sys.excepthook = ExceptionHandler()