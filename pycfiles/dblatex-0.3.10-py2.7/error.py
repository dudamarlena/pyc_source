# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/core/error.py
# Compiled at: 2017-04-03 18:58:57
import sys, traceback

class ErrorHandler(object):
    """
    Object in charge to handle any error occured during the dblatex
    transformation process. The first mandatory argument is the <object>
    that signaled the error.
    """

    def __init__(self):
        pass

    def signal(self, object, *args, **kwargs):
        failure_track('Unexpected error occured')


_current_handler = None
_dump_stack = False

def get_errhandler():
    global _current_handler
    if not _current_handler:
        _current_handler = ErrorHandler()
    return _current_handler


def set_errhandler(handler):
    global _current_handler
    if not isinstance(handler, ErrorHandler):
        raise ValueError('%s is not an ErrorHandler' % handler)
    _current_handler = handler


def signal_error(*args, **kwargs):
    get_errhandler().signal(*args, **kwargs)


def failure_track(msg):
    global _dump_stack
    print >> sys.stderr, msg
    if _dump_stack:
        traceback.print_exc()


def failed_exit(msg, rc=1):
    failure_track(msg)
    sys.exit(rc)


def dump_stack():
    global _dump_stack
    _dump_stack = True