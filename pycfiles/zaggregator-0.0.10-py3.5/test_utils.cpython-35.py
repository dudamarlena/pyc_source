# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/tests/test_utils.py
# Compiled at: 2018-07-09 22:50:46
# Size of source mod 2**32: 8876 bytes
import unittest
from fuzzywuzzy import fuzz, StringMatcher
import psutil, os, sys
from multiprocessing import Process
import time, random, inspect, logging, zaggregator.utils as utils, zaggregator.tests as tests
from zaggregator.procbundle import ProcBundle
from zaggregator.procmirror import ProcessMirror
from zaggregator.proctable import ProcTable as ProcessTable

class TestZaggregatorUtils(tests.TestCase):
    fuzzy_string_sets = (
     [
      '/usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf',
      '/usr/sbin/zabbix_agentd: collector [idle 1 sec]',
      '/usr/sbin/zabbix_agentd: listener #1 [waiting for connection]',
      '/usr/sbin/zabbix_agentd: listener #2 [waiting for connection]',
      '/usr/sbin/zabbix_agentd: listener #3 [waiting for connection]',
      '/usr/sbin/zabbix_agentd: active checks #1 [idle 1 sec]'],
     [
      'postgres: checkpointer process',
      'postgres: writer process',
      'postgres: wal writer process',
      'postgres: autovacuum launcher process',
      'postgres: stats collector process'],
     [
      'php-fpm: pool main',
      'php-fpm: pool main',
      'php-fpm: pool main',
      'php-fpm: pool main'])
    fuzzy_string_sets_nomatch = (
     [
      '/usr/sbin/zabbix_agentd: active checks #1 [idle 1 sec]',
      'postgres: checkpointer process',
      'php-fpm: pool main'],
     [
      'YK1UYU2C: child#0',
      'LCAR8XLT: child#1',
      '6I6P9FKE: child#2',
      '4ZTJ1YEH: child#3',
      '1Y261N7W: child#4',
      'unittest: master'])

    def test_fuzzy_match_seq(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        for i in self.fuzzy_string_sets:
            self.assertTrue(utils.fuzzy_sequence_match(i))

        for i in self.fuzzy_string_sets_nomatch:
            self.assertFalse(utils.fuzzy_sequence_match(i))

    def test_fuzzy_match(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        for fuzzy_strings in self.fuzzy_string_sets:
            for i in range(len(fuzzy_strings) - 1):
                self.assertTrue(utils.fuzzy_match(*fuzzy_strings[i:i + 2]))

    def test_fuzzy_namesearch(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        r = []
        for s in self.fuzzy_string_sets:
            r.append(utils.reduce_sequence(s))

        r1 = [
         '/usr/sbin/zabbix_agentd',
         'postgres',
         'php-fpm: pool main']
        self.assertTrue(r == r1)

    def test_is_proc_group_parent(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittests'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        self.assertTrue(utils.is_proc_group_parent(psutilproc))
        bunch.stop()

    def test_proc_is_not_group_parent(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittests-np'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, israndom=True)
        self.assertFalse(utils.is_proc_group_parent(psutilproc))
        bunch.stop()

    def test_parent_has_single_child(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-sc'
        bunch, myproc, psutilproc = tests.bunchproto.start(bname, israndom=random.choice((true, false)), nchildren=1)
        self.assertTrue(utils.parent_has_single_child(psutilproc.children()[0]))
        bunch.stop()

    def test_parent_has_single_child(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-nsc'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, israndom=random.choice((True,
                                                                                          False)), nchildren=2)
        self.assertFalse(utils.parent_has_single_child(psutilproc.children()[0]))
        bunch.stop()

    def test_parent_has_single_child_false(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-nscf'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, israndom=random.choice((True,
                                                                                          False)), nchildren=1)
        (ProcessMirror,)
        self.assertTrue(utils.parent_has_single_child(psutilproc.children()[0]))
        bunch.stop()

    def test_parent_has_single_child_init(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        psutilproc = random.choice(psutil.Process(pid=1).children())
        self.assertFalse(utils.parent_has_single_child(psutilproc))

    def test_parent_has_single_child_chain(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-ch'
        nproc = random.choice([i for i in range(2, 10)])
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, nchildren=nproc)
        pt = ProcessTable()
        bundle = ProcBundle(ProcessMirror(psutilproc, pt), pt=pt)
        bunch.stop()

    def test_is_kernel_thread_false(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-kth'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, israndom=random.choice((True,
                                                                                          False)), nchildren=1)
        self.assertFalse(utils.is_kernel_thread(psutilproc))
        bunch.stop()

    def test_is_kernel_thread_true(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        pt = ProcessTable()
        proc = ProcessMirror(psutil.Process(pid=2), pt)
        self.assertTrue(utils.is_kernel_thread(proc))

    def test_is_leaf_process_true(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-lpt'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, israndom=random.choice((True,
                                                                                          False)), nchildren=1)
        self.assertTrue(utils.is_leaf_process(psutilproc.children()[0]))
        bunch.stop()

    def test_is_leaf_process_false(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-lpf'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname, israndom=random.choice((True,
                                                                                          False)), nchildren=2)
        self.assertFalse(utils.is_leaf_process(psutilproc))
        self.assertFalse(utils.is_leaf_process(psutilproc.children()[0]))
        bunch.stop()

    def test_is_proc_in_bundle(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = 'unittest-ipib'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        pt = ProcessTable()
        bundle = ProcBundle(ProcessMirror(psutilproc, pt), pt=pt)
        proc = psutilproc.children()[0]
        bunch.stop()

    def test_is_proc_in_bundle_false(self):
        logging.debug('======= %s ======' % inspect.stack()[0][3])
        bname = '1-unittest-ipibf'
        bunch, myproc, psutilproc = tests.BunchProto.start(bname)
        bname = '2-unittest-ipibf'
        bunch2, myproc2, psutilproc2 = tests.BunchProto.start(bname)
        pt = ProcessTable()
        bundle = ProcBundle(ProcessMirror(psutilproc, pt), pt=pt)
        proc = psutilproc.children()[0]
        self.assertFalse(utils.is_proc_in_bundle(myproc2, bundle))
        bunch.stop()
        bunch2.stop()


if __name__ == '__main__':
    run_test_module_by_name(__file__)