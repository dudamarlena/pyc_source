# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/profiling.py
# Compiled at: 2013-11-12 16:48:22
"""
Run this function as main to calibrate your profile.OptionParser

TODO: save the file created into tmp automatically, and have the profile_function
automatically grab the value (and create it if necessary)

Some Notes:
    out = cProfile.runctx('self.function()', globals(),
                          locals(), 'development')
    self._profiler.strip_dirs().sort_stats('cumulative').print_stats()
    return out

"""
from __future__ import division
SHELVE = 'calibration.pcl'
CALIBRATION_VARIABLE = 'calibration'
import pdb, shelve, math, cProfile, profile, pstats

def profile_function(function, name, *args, **kwargs):
    """Run like this:
        profile_name = 'example'
        out = prilfe_function('myfunction', profile_name , globals(), locals(),
                             1,2,3,4,5,6, 'first keyword' = 'first')
        print_profile(profile_name)
        # do stuff with out
    """
    prof = cProfile.Profile()
    retval = prof.runcall(function, *args, **kwargs)
    prof.dump_stats(name)
    print_profile(name)
    return retval


def print_profile(name):
    p = pstats.Stats(name)
    p.strip_dirs().sort_stats('cumulative').print_stats()


def calibrate_profiler():
    """The object of this exercise is to get a fairly consistent result.
    If your computer is very fast, or your timer function has poor resolution,
    you might have to pass 100000, or even 1000000, to get consistent results.
    http://docs.python.org/2/library/profile.html
    """
    pr = profile.Profile()
    for n in xrange(4, 6):
        times = 10 ** n
        a = []
        for i in range(5):
            a.append(pr.calibrate(times))

        print 'Are these numbers roughly the same? (y or n)'
        for n in a:
            print n

        an = raw_input('Answer: ')
        if an == 'y':
            break
    else:
        print 'Could not calibrate profiler'
        return

    d = shelve.open(SHELVE)
    d[CALIBRATION_VARIABLE] = sum(a) / len(a)


if __name__ == '__main__':
    calibrate_profiler()