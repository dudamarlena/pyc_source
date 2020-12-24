# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/utils/multiprocessing_wrapper.py
# Compiled at: 2012-12-26 15:42:47
"""
    This module provides a set of methods for handling multi-threading patterns more easily.

    >>> import src.utils.multiprocessing_wrapper as mpw
    >>> mpw.build_thread_pool(['one','two'],len,2,[])
    [2,2]
"""
import multiprocessing as mp, multiprocessing.pool as mp_pool, math
__author__ = 'ryan faulkner'
__date__ = '12/12/2012'
__license__ = 'GPL (version 2 or later)'

def build_thread_pool(data, callback, k, args):
    """
        Handles initializing, executing, and cleanup for thread pools
    """
    n = int(math.ceil(float(len(data)) / k))
    arg_list = list()
    for i in xrange(k):
        arg_list.append([data[i * n:(i + 1) * n], args])

    arg_list = filter(lambda x: len(x[0]), arg_list)
    if not arg_list:
        return []
    pool = NonDaemonicPool(processes=len(arg_list))
    results = list()
    if arg_list:
        for elem in pool.map(callback, arg_list):
            if hasattr(elem, '__iter__'):
                results.extend(elem)
            else:
                results.extend([elem])

    pool.terminate()
    return results


class NoDaemonicProcess(mp.Process):

    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonicPool(mp_pool.Pool):
    Process = NoDaemonicProcess