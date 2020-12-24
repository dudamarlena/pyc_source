# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/culprit.py
# Compiled at: 2019-08-16 17:27:45
"""
This file implements the legacy culprit system.  The culprit at this point is
just used as a fallback if no transaction is set.  When a transaction is set
the culprit is overriden by the transaction value.

Over time we want to fully phase out the culprit.  Until then this is the
code that generates it.
"""
from __future__ import absolute_import
from sentry.constants import MAX_CULPRIT_LENGTH
from sentry.utils.safe import get_path
from sentry.utils.strings import truncatechars

def generate_culprit(data):
    platform = data.get('platform')
    exceptions = get_path(data, 'exception', 'values', filter=True)
    if exceptions:
        last_exception = get_path(exceptions, -1)
        if get_path(last_exception, 'mechanism', 'synthetic'):
            return ''
        stacktraces = [ e['stacktrace'] for e in exceptions if get_path(e, 'stacktrace', 'frames') ]
    else:
        stacktrace = data.get('stacktrace')
        if stacktrace and stacktrace.get('frames'):
            stacktraces = [
             stacktrace]
        else:
            stacktraces = None
    culprit = None
    if not culprit and stacktraces:
        culprit = get_stacktrace_culprit(get_path(stacktraces, -1), platform=platform)
    if not culprit and data.get('request'):
        culprit = get_path(data, 'request', 'url')
    return truncatechars(culprit or '', MAX_CULPRIT_LENGTH)


def get_stacktrace_culprit(stacktrace, platform):
    default = None
    for frame in reversed(stacktrace['frames']):
        if not frame:
            continue
        if frame.get('in_app'):
            culprit = get_frame_culprit(frame, platform=platform)
            if culprit:
                return culprit
        elif default is None:
            default = get_frame_culprit(frame, platform=platform)

    return default


def get_frame_culprit(frame, platform):
    platform = frame.get('platform') or platform
    if platform in ('objc', 'cocoa', 'native'):
        return frame.get('function') or '?'
    fileloc = frame.get('module') or frame.get('filename')
    if not fileloc:
        return ''
    if platform in ('javascript', 'node'):
        return '%s(%s)' % (frame.get('function') or '?', fileloc)
    return '%s in %s' % (fileloc, frame.get('function') or '?')