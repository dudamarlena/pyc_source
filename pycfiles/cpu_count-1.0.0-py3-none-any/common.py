# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/fab/Documents/cpu_cores/cpu_cores/common.py
# Compiled at: 2013-08-31 05:10:42
import sys

class CPUCoresCounter(object):
    platform = None
    _physical_cores_count = None
    _physical_processors_count = None

    def _count(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def factory(cls, force_platform=None):
        if force_platform is not None:
            cls.platform = force_platform
        else:
            cls.platform = sys.platform
        if cls.platform.startswith('darwin'):
            from cpu_cores.darwin import DarwinCPUCoresCounter
            return DarwinCPUCoresCounter()
        else:
            if cls.platform.startswith('linux'):
                from cpu_cores.linux import LinuxCPUCoresCounter
                return LinuxCPUCoresCounter()
            raise NotImplementedError('unsupported platform type [%s]' % cls.platform)
            return

    def _check_counting_or_do_it(self):
        if self._physical_processors_count is None or self._physical_cores_count is None:
            self._count()
        return

    def get_physical_cores_count(self):
        self._check_counting_or_do_it()
        return self._physical_cores_count

    def get_physical_processors_count(self):
        self._check_counting_or_do_it()
        return self._physical_processors_count