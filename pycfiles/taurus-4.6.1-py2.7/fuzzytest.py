# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/fuzzytest.py
# Compiled at: 2019-08-19 15:09:30
"""Utility functions to deal with non-ideal (fuzzy) tests"""
from __future__ import print_function
from future.utils import string_types

def loopTest(testname, maxtries=100, maxfails=10):
    """Run a test `maxtries` times or until it fails `maxfails` times and
    report the number of tries and failures.

    :param testname: (str) test name. see:
                     :meth:`unittest.TestLoader.loadTestsFromName`
    :param maxtries: (int) maximum number of runs
    :param maxfails: (int) maximum number of failed runs

    :return: (tuple) a tuple of ints: tries, failures
    """
    import unittest
    suite = unittest.defaultTestLoader.loadTestsFromName(testname)
    runner = unittest.TextTestRunner(verbosity=0)
    i, f = (0, 0)
    while f < maxfails and i < maxtries:
        i += 1
        result = runner.run(suite)
        if not result.wasSuccessful():
            f += 1

    return (
     i, f)


def loopSubprocess(target, maxtries=100, maxfails=10, okvalues=(0, ), args=(), kwargs=None):
    """Run a callable as a subprocess `maxtries` times or until it fails
    `maxfails` times and report the number of tries and failures.
    The callable is run as a subprocess and it is considered to run fine if
    the subprocess exit code is in the okValues list.

    :param target: (callable) a callable test
    :param maxtries: (int) maximum number of runs
    :param maxfails: (int) maximum number of failed runs
    :param okvalues: (seq) a sequence containing exit values of cmd which
                     are considered to be successful runs.
    :param args: (seq) arguments for running the target function
    :param kwargs: (dict) keyword arguments for running the target function

    :return: (tuple) a tuple of ints: tries, failures
    """
    if kwargs is None:
        kwargs = {}
    from multiprocessing import Process
    i, f = (0, 0)
    while f < maxfails and i < maxtries:
        i += 1
        p = Process(target=target, args=args, kwargs=kwargs)
        p.start()
        p.join()
        if p.exitcode not in okvalues:
            f += 1

    return (
     i, f)


def calculateTestFuzziness(test, maxtries=100, maxfails=10, **kwargs):
    """Estimate the fuzziness of a test by running it many times and counting
    the failures. In this context, we assume that there is an underlying
    problem and but that the test is not perfect and only fails (triggers the
    problem) with a certain failure rate.

    :param testname: (str) test name. see:
                     :meth:`unittest.TestLoader.loadTestsFromName`
    :param maxtries: (int) maximum number of runs
    :param maxfails: (int) maximum number of failed runs

    :return: (tuple) a tuple (f,df,n) where f is the failure rate, df is its
             standard deviation, and n is the number of consecutive
             times that the test should be passed to have a confidence>99%%
             that the bug is fixed'
    """
    print(('Running the test %i times (or until it fails %i times)' + 'to estimate the failure rate') % (maxtries, maxfails))
    import numpy
    if isinstance(test, string_types):
        tries, fails = loopTest(test, maxtries=maxtries, maxfails=maxfails)
    else:
        tries, fails = loopSubprocess(test, maxtries=maxtries, maxfails=maxfails, **kwargs)
    r = float(fails) / tries
    dr = numpy.sqrt(fails) / tries
    print('Failure rate = %g +/- %g  (%i/%i)' % (r, dr, fails, tries))
    n = numpy.ceil(numpy.log(0.01) / numpy.log(1 - (r - dr)))
    print(('Number of consecutive times that the test should be passed ' + 'to have a confidence>99%% that the bug is fixed: %g') % n)
    return (r, dr, n)


if __name__ == '__main__':

    def kk():
        from numpy.random import randint, seed
        seed()
        k = randint(3)
        if not k:
            exit(1)


    print(calculateTestFuzziness(kk))