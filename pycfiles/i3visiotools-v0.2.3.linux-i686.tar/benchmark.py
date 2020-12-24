# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/benchmark.py
# Compiled at: 2014-12-25 06:48:18
import time
from multiprocessing import Pool
import logging, urllib2

def testFunctionWeb():
    """
                Benchmarcking function...
        """
    resp = urllib2.urlopen('http://www.i3visio.com')
    html = resp.read()


def testFunction2():
    """
                Benchmarcking function...
        """
    a = 1
    for i in range(1000):
        a += 1


def multi_run_wrapper(args):
    """ 
        Wrapper for being able to launch all the threads of getPageWrapper. 
        Parameters:
                We receive the parameters for getPageWrapper as a tuple.
        """
    return testFunctionWeb(*args)


def doBenchmark(plats):
    """
                Perform the benchmark...
        """
    logger = logging.getLogger('i3visiotools')
    res = {}
    args = []
    tries = [
     1, 4, 8, 16, 24, 32, 40, 48, 56, 64]
    logger.info('The test is starting recovering webpages by creating the following series of threads: ' + str(tries))
    for i in tries:
        print 'Testing creating ' + str(i) + ' simultaneous threads...'
        t0 = time.clock()
        pool = Pool(i)
        poolResults = pool.map(multi_run_wrapper, args)
        t1 = time.clock()
        res[i] = t1 - t0
        print str(i) + '\t' + str(res[i]) + '\n'

    return res