# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/tests/test_proctable.py
# Compiled at: 2018-08-01 11:30:05
# Size of source mod 2**32: 3354 bytes
import unittest, psutil, time, logging, random, inspect, signal, os, zaggregator, zaggregator.utils as utils, zaggregator.tests as tests, zaggregator.procbundle as pb
from zaggregator.procbundle import ProcBundle
from zaggregator.proctable import ProcTable
from zaggregator.procmirror import ProcessMirror
from zaggregator.tests import cycle
import zaggregator.config
zaggregator.config.DEFAULT_INTERVAL = 0.1

class TestProcMirror(tests.TestCase):

    def test_ProcessMirror_alive(self):
        proc = psutil.Process(pid=os.getpid())
        mirror = ProcessMirror(proc, None)
        self.assertTrue(mirror.alive)
        self.assertTrue(mirror.alive == proc.is_running())

    def test_ProcessMirror_pid(self):
        proc = psutil.Process(pid=os.getpid())
        mirror = ProcessMirror(proc, None)
        self.assertTrue(mirror.pid == proc.pid == os.getpid())

    def test_ProcessMirror_set_pcpu(self):
        proc = psutil.Process(pid=os.getpid())
        mirror = ProcessMirror(proc, None)
        mirror.set_pcpu(0.123456)
        self.assertTrue(mirror.pcpu == 0.123456)


class TestProcTable(tests.TestCase):

    def test_ProcTable_mirror_by_pid(self):
        pt = ProcTable()
        proc = psutil.Process(pid=os.getpid())
        self.assertTrue(pt.mirror_by_pid(os.getpid()).pid == os.getpid())

    def test_ProcTable_mirrors_by_pgid(self):
        bname = 'unittest-ptmbp'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        pt = ProcTable()
        pgid = os.getpgid(psutilproc.pid)
        self.assertTrue(len(list(filter(None, [p._pgid != pgid for p in pt.mirrors_by_pgid(pgid)]))) == 0)
        bunch.stop()

    def test_ProcTable_mirror_by_pid(self):
        bname = 'unittest-ptmbp2'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        pt = ProcTable()
        self.assertIsInstance(pt.mirror_by_pid(psutilproc.pid), ProcessMirror)
        bunch.stop()

    def test_ProcTable_pidm(self):
        bname = 'unittest-pm'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        pt = ProcTable()
        self.assertIsInstance(pt.mirror_by_pid(psutilproc.pid).pidm(psutilproc.pid), ProcessMirror)
        bunch.stop()

    def test_ProcTable_children(self):
        bname = 'unittest-pm'
        nchildren = 5
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=5)
        pt = ProcTable()
        m = pt.mirror_by_pid(psutilproc.pid)
        self.assertTrue(len(m.children()) == nchildren)
        self.assertIsInstance(m.children()[0], ProcessMirror)
        bunch.stop()

    def test_ProcTable_test(self):
        bname = 'unittest-t'
        nchildren = 5
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=5)
        pt = ProcTable()
        bunch.stop()

    def test_ProcTable_get_top_5s(self):
        bname = 'unittest-ptgt5s'
        nchildren = 10
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=5)
        pt = ProcTable()
        top5 = pt.get_top_5s()
        self.assertTrue(len(top5) > 5)
        bunch.stop()


if __name__ == '__main__':
    tests.run_test_module_by_name(__file__)