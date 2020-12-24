# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/faya/lib/__muti.py
# Compiled at: 2018-06-29 04:14:54
# Size of source mod 2**32: 1046 bytes
from multiprocessing import Pool, Manager

class Multithread(object):

    def __init__(self):
        self.queue = _Queue()

    @staticmethod
    def execute(f, data_list):
        pool = Pool()
        pool.map(f, data_list)
        pool.close()
        pool.join()


class _Queue(object):

    def __init__(self):
        self._Queue__q = Manager().Queue()
        self._Queue__f = None
        self._Queue__dl = []
        self._Queue__len = 0

    def __put_q(self):
        [self._Queue__q.put(each) for each in self._Queue__dl]

    def execute(self, f, datalist):
        self._Queue__dl = datalist
        self._Queue__len = range(0, len(datalist))
        self._Queue__f = f
        pool = Pool()
        self._Queue__put_q()
        pool.map(self._dummy, self._Queue__len)
        pool.close()
        pool.join()

    def _dummy(self, placeholder):
        self._Queue__f(self._Queue__q.get())


if __name__ == '__main__':
    l = range(0, 5)

    def p(n):
        print(n)


    mp = Multithread()
    mp.execute(p, l)
    print('==========q' + '==========')
    mp.queue.execute(p, l)