# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/trace.py
# Compiled at: 2007-03-21 14:34:41
"""Efficient tracing of internal Schevo events.

Usage::

  from schevo.trace import log
  assert log(level, message)

The assert is necessary to completely remove calls to the tracer
in production code.

For copyright, license, and warranty, see bottom of file.
"""
import inspect, sys
from schevo.lib.optimize import do_not_optimize
TRACE_TO = sys.stderr
_history = []
monitor_level = 0
monitor_prefix = '#'

def history(max_level):
    """Return a generator for items from `_history` up to and including
    those at `max_level`."""
    assert isinstance(max_level, int)
    return ((level, where, messages) for (level, where, messages) in _history if level <= max_level)


def print_history(max_level):
    """Print a pretty version of the results of `history(max_level)`."""
    for (level, where, messages) in history(max_level):
        print >> TRACE_TO, monitor_prefix, where,
        if level > 1:
            print >> TRACE_TO, '--' * (level - 1),
        for m in messages:
            print >> TRACE_TO, m,

        print >> TRACE_TO


@do_not_optimize
def log(level, *messages):
    """Append `message` at `level` to `_history`, outputting to stderr
    if desired."""
    if not monitor_level:
        pass
    assert isinstance(level, int)
    frame = sys._getframe(1)
    finfo = inspect.getframeinfo(frame)
    filename = finfo[0]
    funcname = finfo[2]
    modulename = inspect.getmodulename(filename)
    where = '%s.%s:' % (modulename, funcname)
    if _history is not None:
        _history.append((level, where, messages))
    if level <= monitor_level:
        print >> TRACE_TO, monitor_prefix, where,
        if level > 1:
            print >> TRACE_TO, '--' * (level - 1),
        for m in messages:
            print >> TRACE_TO, m,

        print >> TRACE_TO
    return True