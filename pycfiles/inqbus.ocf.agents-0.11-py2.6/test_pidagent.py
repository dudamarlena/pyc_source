# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/test/test_pidagent.py
# Compiled at: 2011-11-29 11:36:01
import nose.tools, os
from inqbus.ocf.agents.pidagent import PIDAgent
from inqbus.ocf.agents.test import data
TEST_CLASSES = [
 PIDAgent]

class TestPidagentWithDummyDaemon:

    def setUp(self):
        """
        Use the dummy_daemon
        """
        os.environ['OCF_RESKEY_pid_file'] = '/tmp/dummy_daemon.pid'
        os.environ['OCF_RESKEY_executable'] = './bin/dummy_daemon'

    def test_ocftester_actions(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            for (action, error) in data.OCFTESTER_ACTIONS_RETCODES:
                vector = [
                 'agent', action]
                yield (self.do_ocftester_actions, TestClass, vector, error)

    def do_ocftester_actions(self, TestClass, vector, error):
        self.TEST_CLASSES = TEST_CLASSES
        if not error:
            assert TestClass().run(vector) == True
        else:
            nose.tools.assert_raises(error, TestClass().run, vector)