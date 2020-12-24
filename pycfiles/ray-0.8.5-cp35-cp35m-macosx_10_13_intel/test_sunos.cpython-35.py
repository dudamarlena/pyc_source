# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/nz/vv4_9tw56nv9k3tkvyszvwg80000gn/T/pip-unpacked-wheel-c6tqtva7/psutil/tests/test_sunos.py
# Compiled at: 2020-05-06 17:45:43
# Size of source mod 2**32: 1294 bytes
"""Sun OS specific tests."""
import os, psutil
from psutil import SUNOS
from psutil.tests import sh
from psutil.tests import unittest

@unittest.skipIf(not SUNOS, 'SUNOS only')
class SunOSSpecificTestCase(unittest.TestCase):

    def test_swap_memory(self):
        out = sh('env PATH=/usr/sbin:/sbin:%s swap -l' % os.environ['PATH'])
        lines = out.strip().split('\n')[1:]
        if not lines:
            raise ValueError('no swap device(s) configured')
        total = free = 0
        for line in lines:
            line = line.split()
            t, f = line[-2:]
            total += int(int(t) * 512)
            free += int(int(f) * 512)

        used = total - free
        psutil_swap = psutil.swap_memory()
        self.assertEqual(psutil_swap.total, total)
        self.assertEqual(psutil_swap.used, used)
        self.assertEqual(psutil_swap.free, free)

    def test_cpu_count(self):
        out = sh('/usr/sbin/psrinfo')
        self.assertEqual(psutil.cpu_count(), len(out.split('\n')))


if __name__ == '__main__':
    from psutil.tests.runner import run
    run(__file__)