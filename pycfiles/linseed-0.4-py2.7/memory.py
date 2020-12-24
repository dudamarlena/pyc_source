# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/memory.py
# Compiled at: 2012-02-12 04:59:14
import psutil

class Memory(object):
    """Information on the state of main memory for a system.
    """

    def __init__(self):
        self._usage = psutil.phymem_usage()

    @property
    def total(self):
        """Total physical memory."""
        return self._usage.total

    @property
    def used(self):
        """Memory currently in use."""
        return self._usage.used

    @property
    def free(self):
        """Memory currently free."""
        return self._usage.free

    @property
    def percent(self):
        """Percent of memory currently in use."""
        return self._usage.percent

    @staticmethod
    def name():
        return 'linseed_memory'

    @staticmethod
    def description():
        return 'Current memory utilization (%)'

    def __str__(self):
        return ('Memory(total={}, used={}, free={}, percent={})').format(self.total, self.used, self.free, self.percent)


class Swap(object):

    def __init__(self):
        self._usage = psutil.virtmem_usage()

    @property
    def total(self):
        """Total swap space."""
        return self._usage.total

    @property
    def used(self):
        """Swap currently in use."""
        return self._usage.used

    @property
    def free(self):
        """Swap currently free."""
        return self._usage.free

    @property
    def percent(self):
        """Percent of swap currently in use."""
        return self._usage.percent

    @staticmethod
    def name():
        return 'linseed_swap'

    @staticmethod
    def description():
        return 'Current swap usage (%)'

    def __str__(self):
        return ('Swap(total={}, used={}, free={}, percent={})').format(self.total, self.used, self.free, self.percent)