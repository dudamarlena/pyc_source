# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/memory.py
# Compiled at: 2010-01-20 17:55:02
import gc
PAGE_SIZE = 4096

def getMemoryLimit():
    """
    Get current memory limit in bytes.

    Return None on error.
    """
    return


def setMemoryLimit(max_mem):
    """
    Set memory limit in bytes.
    Use value 'None' to disable memory limit.

    Return True if limit is set, False on error.
    """
    return False


def getMemorySize():
    """
    Read currenet process memory size: size of available virtual memory.
    This value is NOT the real memory usage.

    This function only works on Linux (use /proc/self/statm file).
    """
    try:
        statm = open('/proc/self/statm').readline().split()
    except IOError:
        return

    return int(statm[0]) * PAGE_SIZE


def clearCaches():
    """
    Try to clear all caches: call gc.collect() (Python garbage collector).
    """
    gc.collect()


try:
    from resource import getpagesize, getrlimit, setrlimit, RLIMIT_AS
    PAGE_SIZE = getpagesize()

    def getMemoryLimit():
        try:
            limit = getrlimit(RLIMIT_AS)[0]
            if 0 < limit:
                limit *= PAGE_SIZE
            return limit
        except ValueError:
            return

        return


    def setMemoryLimit(max_mem):
        if max_mem is None:
            max_mem = -1
        try:
            setrlimit(RLIMIT_AS, (max_mem, -1))
            return True
        except ValueError:
            return False

        return


except ImportError:
    pass

def limitedMemory(limit, func, *args, **kw):
    """
    Limit memory grow when calling func(*args, **kw):
    restrict memory grow to 'limit' bytes.

    Use try/except MemoryError to catch the error.
    """
    clearCaches()
    max_rss = getMemorySize()
    if max_rss is not None:
        old_limit = getMemoryLimit()
        limit = max_rss + limit
        limited = setMemoryLimit(limit)
    else:
        limited = False
    try:
        return func(*args, **kw)
    finally:
        if limited:
            setMemoryLimit(old_limit)
        clearCaches()
    return