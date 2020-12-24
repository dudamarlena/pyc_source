# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/volker/workspace/ocf/inqbus.ocf.agents/build/lib.linux-i686-2.6/inqbus/ocf/agents/test/test_openvpn.py
# Compiled at: 2011-11-20 14:31:47
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest, inspect
from inqbus.ocf.agents.openvpn import OpenVPN
from inqbus.ocf.generic.exits import OCF_ERR_UNIMPLEMENTED
from inqbus.ocf.agents.test import data

class TestOpenvpnRun(unittest.TestCase):

    def setUp(self):
        self.TEST_CLASSES = [
         OpenVPN]

    def test_base_actions(self):
        for action in data.BASE_ACTIONS:
            for TestClass in self.TEST_CLASSES:
                vector = [
                 'agent', action]
                self.assertEqual(TestClass().run(vector), True, 'run Method returns True')

    def test_bad_action(self):
        for sysargv in data.BAD_ACTIONS:
            for TestClass in self.TEST_CLASSES:
                self.assertRaises(OCF_ERR_UNIMPLEMENTED, TestClass().run, sysargv)