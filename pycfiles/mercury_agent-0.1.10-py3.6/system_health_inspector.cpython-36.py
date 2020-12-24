# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/inspectors/system_health_inspector.py
# Compiled at: 2019-02-11 13:08:12
# Size of source mod 2**32: 1449 bytes
import unittest, box, mock
from mercury_agent.inspector.inspectors import health
_config = {'agent': {'hardware': {'mce_threshold':10, 
                        'oem':{'hp': {'hpasmcli_path': 'noop'}}}}}

class SysHealthInspector(unittest.TestCase):

    @mock.patch('mercury_agent.inspector.inspectors.health.mcelog')
    @mock.patch('mercury_agent.inspector.inspectors.health.hpasmcli')
    @mock.patch('mercury_agent.inspector.inspectors.health.get_configuration')
    def test_with_hp_error(self, mock_get_config, mock_hpasm, mock_mce):
        device_info = {'dmi': {'sys_vendor': 'HP'}}

        class FakeHP:

            def show_server(self):
                return {'processors': [{'status': 'Nope'}]}

            def show_dimm(self):
                return []

            def show_powersupply(self):
                return []

        mock_mce.count_logged_events = mock.Mock(return_value=0)
        mock_get_config.return_value = box.Box(_config)
        mock_hpasm.HPASMCLI = mock.Mock(return_value=(FakeHP()))
        mock_hp_obj = mock_hpasm.HPASMCLI()
        print(mock_hp_obj.show_server())
        print(health.system_health_inspector(device_info))