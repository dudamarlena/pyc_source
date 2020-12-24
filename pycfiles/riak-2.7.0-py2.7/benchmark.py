# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/benchmark.py
# Compiled at: 2016-10-17 19:06:50
from __future__ import print_function
import os, gc, sys, traceback
__all__ = [
 'measure', 'measure_with_rehearsal']

def measure_with_rehearsal():
    """
    Runs a benchmark when used as an iterator, injecting a garbage
    collection between iterations. Example::

        for b in riak.benchmark.measure_with_rehearsal():
            with b.report("pow"):
                for _ in range(10000):
                    math.pow(2,10000)
            with b.report("factorial"):
                for i in range(100):
                    math.factorial(i)
    """
    return Benchmark(True)


def measure():
    """
    Runs a benchmark once when used as a context manager. Example::

        with riak.benchmark.measure() as b:
            with b.report("pow"):
                for _ in range(10000):
                    math.pow(2,10000)
            with b.report("factorial"):
                for i in range(100):
                    math.factorial(i)
    """
    return Benchmark()


class Benchmark(object):
    """
    A benchmarking run, which may consist of multiple steps. See
    measure_with_rehearsal() and measure() for examples.
    """

    def __init__(self, rehearse=False):
        """
        Creates a new benchmark reporter.

        :param rehearse: whether to run twice to take counter the effects
           of garbage collection
        :type rehearse: boolean
        """
        self.rehearse = rehearse
        if rehearse:
            self.count = 2
        else:
            self.count = 1
        self._report = None
        return

    def __enter__(self):
        if self.rehearse:
            raise ValueError('measure_with_rehearsal() cannot be used in with statements, use measure() or the for..in statement')
        print_header()
        self._report = BenchmarkReport()
        self._report.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._report:
            return self._report.__exit__(exc_type, exc_val, exc_tb)
        else:
            print
            return True

    def __iter__(self):
        return self

    def next(self):
        """
        Runs the next iteration of the benchmark.
        """
        if self.count == 0:
            raise StopIteration
        elif self.count > 1:
            print_rehearsal_header()
        else:
            if self.rehearse:
                gc.collect()
                print('-' * 59)
                print()
            print_header()
        self.count -= 1
        return self

    def __next__(self):
        return self.next()

    def report(self, name):
        """
        Returns a report for the current step of the benchmark.
        """
        self._report = None
        return BenchmarkReport(name)


def print_rehearsal_header():
    """
    Prints the header for the rehearsal phase of a benchmark.
    """
    print
    print('Rehearsal -------------------------------------------------')


def print_report(label, user, system, real):
    """
    Prints the report of one step of a benchmark.
    """
    print(('{:<12s} {:12f} {:12f} ( {:12f} )').format(label, user, system, real))


def print_header():
    """
    Prints the header for the normal phase of a benchmark.
    """
    print(('{:<12s} {:<12s} {:<12s} ( {:<12s} )').format('', 'user', 'system', 'real'))


class BenchmarkReport(object):
    """
    A labeled step in a benchmark. Acts as a context-manager, printing
    its timing results when the context exits.
    """

    def __init__(self, name='benchmark'):
        self.name = name
        self.start = None
        return

    def __enter__(self):
        self.start = os.times()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            user1, system1, _, _, real1 = self.start
            user2, system2, _, _, real2 = os.times()
            print_report(self.name, user2 - user1, system2 - system1, real2 - real1)
        else:
            if exc_type is KeyboardInterrupt:
                return False
            msg = 'EXCEPTION! type: %r val: %r' % (exc_type, exc_val)
            print(msg, file=sys.stderr)
            traceback.print_tb(exc_tb)
        if exc_type is None:
            return True
        else:
            return False