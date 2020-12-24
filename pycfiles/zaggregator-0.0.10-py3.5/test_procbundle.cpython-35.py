# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/tests/test_procbundle.py
# Compiled at: 2018-07-31 11:08:30
# Size of source mod 2**32: 4552 bytes
import unittest, psutil, time, logging, random, inspect, signal, zaggregator, zaggregator.utils as utils, zaggregator.tests as tests, zaggregator.procbundle as pb
from zaggregator.procbundle import ProcBundle
from zaggregator.proctable import ProcTable
from zaggregator.procmirror import ProcessMirror
from zaggregator.tests import cycle
zaggregator.procbundle.DEFAULT_INTERVAL = 0.1

class TestProcBundle(tests.TestCase):

    def test_ProcessBundle_name(self):
        bname = 'unittest-pb'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        procs = psutilproc.children()
        procs.append(psutilproc)
        pt = ProcTable()
        procs = [ProcessMirror(p, pt) for p in procs]
        bundle = ProcBundle(procs, pt=pt)
        self.assertTrue(bundle.bundle_name == bname)
        bunch.stop()

    def test_ProcTable_get_bundle_names(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        try:
            table = ProcTable()
            logging.debug('Bundle names: {}'.format(table.get_bundle_names()))
        except psutil._exceptions.AccessDenied as e:
            logging.error(e)
            logging.error('Some tests require root priveleges')

    def test_ProcBundle_stats(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-pbs'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        pt = ProcTable()
        bundle = pt.get_bundle_by_name(pt.get_bundle_names()[0])
        self.assertIsInstance(bundle.get_n_ctx_switches_vol(), int)
        self.assertIsInstance(bundle.get_n_ctx_switches_invol(), int)
        self.assertIsInstance(bundle.get_memory_info_rss(), int)
        self.assertIsInstance(bundle.get_memory_info_vms(), int)
        self.assertIsInstance(bundle.get_cpu_percent(), float)
        bunch.stop()

    def test_get_idle(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        p = ProcTable()
        self.assertIsInstance(p.get_idle(), float)
        bname = 'unittest-gi'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=2, func=cycle)
        p = ProcTable()
        self.assertTrue(p.get_idle() < 10.0)
        bunch.stop()

    def test_get_pcpu_busy(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-gpcpb'
        procname = 'sh:./test.sh'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=2, func=cycle)
        p = ProcTable()
        time.sleep(0.1)
        bundle = p.get_bundle_by_name(procname)
        pcpu = bundle.pcpu
        pcpu_threshold = 75
        if pcpu <= pcpu_threshold:
            print('pcpu value: {}'.format(pcpu))
        self.assertTrue(pcpu > pcpu_threshold)
        bunch.stop()

    def test_name_from_proctitles(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-nfpt'
        procname = 'sh:./test.sh'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=2, func=cycle)
        p = ProcTable()
        time.sleep(0.1)
        bundle = p.get_bundle_by_name(bname)
        bunch.stop()


if __name__ == '__main__':
    run_test_module_by_name(__file__)