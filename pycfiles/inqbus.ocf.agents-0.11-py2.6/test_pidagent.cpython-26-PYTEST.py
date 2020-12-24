# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/volker/workspace/ocf/inqbus.ocf.agents/build/lib.linux-i686-2.6/inqbus/ocf/agents/test/test_pidagent.py
# Compiled at: 2011-11-20 15:04:51
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest, os, sys
from inqbus.ocf.agents.pidagent import PIDAgent
from inqbus.ocf.generic.exits import OCF_ERR_UNIMPLEMENTED
from inqbus.ocf.agents.test import data
from test_openvpn import TestOpenvpnRun
TEST_CLASSES = [
 PIDAgent]

class TestPidagentWithDummyDaemon(TestOpenvpnRun):

    def setUp(self):
        os.environ['OCF_RESKEY_pid_file'] = '/tmp/dummy_daemon.pid'
        os.environ['OCF_RESKEY_executable'] = './bin/dummy_daemon'
        self.TEST_CLASSES = TEST_CLASSES

    def test_base_actions(self):
        for action in data.BASE_ACTIONS:
            for TestClass in self.TEST_CLASSES:
                vector = [
                 'agent', action]
                data.log('\nTesting Class %s with action %s\n' % (TestClass, action))
                self.assertEqual(TestClass().run(vector), True, 'Class %s failed action %s' % (TestClass, action))

    def test_ocftester_actions(self):
        for (action, error) in data.OCFTESTER_ACTIONS_RETCODES:
            for TestClass in self.TEST_CLASSES:
                vector = [
                 'agent', action]
                data.log('Testing Class %s with action %s, error %s' % (TestClass, action, error))
                if not error:
                    self.assertEqual(TestClass().run(vector), True, 'Class %s failed action %s' % (TestClass, action))
                else:
                    self.assertRaises(error, TestClass().run, vector)