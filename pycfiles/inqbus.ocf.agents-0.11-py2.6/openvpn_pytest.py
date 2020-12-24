# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/test/openvpn_pytest.py
# Compiled at: 2011-11-21 17:36:44
import pytest
from inqbus.ocf.agents.openvpn import OpenVPN
from inqbus.ocf.generic.exits import OCF_ERR_UNIMPLEMENTED
from inqbus.ocf.agents.test import data
from inqbus.ocf.agents.test.data import pytest_generate_tests

class TestOpenvpnRun:
    scenarios = data.SCENARIO_OCFTESTER_ACTIONS_RETCODES

    def setup_method(self, method):
        self.TEST_CLASSES = [
         OpenVPN]

    def test_base_actions(self, action, error):
        vector = [
         'agent', action]
        assert self.TEST_CLASSES[0]().run(vector) == True