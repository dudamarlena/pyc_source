# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/edsd/logpeeker.py
# Compiled at: 2016-05-08 02:40:49
"""
edas-detector.logpeeker : peek a log file based on the timestamp, exclude those
information which are before the selected
"""
__author__ = 'Thomas Li <yanliang.lyl@alibaba-inc.com>'
__license__ = 'GNU License'
from edsd import __version__
import re, os, sys, types
from edsd.common import isodt2ts, todaystime, ensure_dir, EDAS_DIRECTORY

def move_patial_log(logfile, start, end=None):
    """Parse a given log file according the start time and end time(be default:
     None), move the filter log lines into a tmp file, and then return the temp
     file's path.
    """
    ensure_dir(EDAS_DIRECTORY)
    tmpname = os.path.join(EDAS_DIRECTORY, os.path.basename(logfile))
    start = isodt2ts(start) if isinstance(start, types.StringType) else start
    end = -1 if end is None else end
    end = isodt2ts(end) if isinstance(end, types.StringType) else end
    with open(tmpname, 'w') as (f):
        for x in filter_log(logfile, start, end):
            f.writelines(x)

    return tmpname


def filter_log(filename, start, end=-1):
    started = False
    with open(filename) as (f):
        for x in f.xreadlines():
            if end == -1:
                pass
            found, isbetween = between(x, start, end)
            if not started and not isbetween:
                continue
            if found and started and not isbetween:
                return
            if not found and started:
                yield x
                continue
            if found and isbetween and not started:
                started = True
            if found and isbetween:
                yield x


def between(l, start, end=-1):
    found, lt = timestamp_in_line(l)
    end = end if end > 0 else sys.maxint
    return (
     found, start <= lt <= end)


p_TIME = re.compile('(\\d{1,2}:\\d{1,2}:\\d{1,2})')
p_DATE = re.compile('(\\d{1,4}[_/-]\\d{1,2}[_/-]\\d{1,4})')

def timestamp_in_line(l):
    g = p_TIME.search(l)
    if g is None:
        return (False, 0)
    else:
        time = g.group(1)
        l = l[:g.end()]
        g = p_DATE.search(l)
        if g is None:
            return (False, todaystime(time))
        date = g.group(1)
        return (g.start() < 12, isodt2ts('%s %s' % (date, time)))