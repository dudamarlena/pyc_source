# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/profiler.py
# Compiled at: 2009-09-07 17:44:28
from hotshot import Profile
from hotshot.stats import load as loadStats
from os import unlink

def runProfiler(func, args=tuple(), kw={}, verbose=True, nb_func=25, sort_by=('cumulative', 'calls')):
    profile_filename = '/tmp/profiler'
    prof = Profile(profile_filename)
    try:
        if verbose:
            print '[+] Run profiler'
        result = prof.runcall(func, *args, **kw)
        prof.close()
        if verbose:
            print '[+] Stop profiler'
            print '[+] Process data...'
        stat = loadStats(profile_filename)
        if verbose:
            print '[+] Strip...'
        stat.strip_dirs()
        if verbose:
            print '[+] Sort data...'
        stat.sort_stats(*sort_by)
        if verbose:
            print
            print '[+] Display statistics'
            print
        stat.print_stats(nb_func)
        return result
    finally:
        unlink(profile_filename)