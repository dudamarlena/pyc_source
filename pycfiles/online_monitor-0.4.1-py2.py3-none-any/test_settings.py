# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/testing/test_settings.py
# Compiled at: 2018-07-05 04:39:41
""" Script to check the settings class of the online monitor.
Since the settings change after the online monitor is used, this
unittests only works on a new installation. The OnlineMonitor.ini
should be untouched.
"""
import unittest, yaml, os
from online_monitor.utils import settings

def create_forwarder_config_yaml(n_converter):
    conf, devices = {}, {}
    for index in range(n_converter):
        devices['DUT%s' % index] = {'kind': 'forwarder', 
           'frontend': 'tcp://127.0.0.1:55%02d' % index, 
           'backend': 'tcp://127.0.0.1:55%02d' % (index + 1)}

    conf['converter'] = devices
    return yaml.dump(conf, default_flow_style=False)


class TestSettings(unittest.TestCase):

    def test_entities_settings(self):
        settings.add_converter_path('C:\\\\test\\\\converter\\\\path')
        settings.add_receiver_path('/home/receiver/path')
        settings.add_producer_sim_path('test/producer_sim/path')
        self.assertTrue('C:\\\\test\\\\converter\\\\path' in settings.get_converter_path())
        self.assertTrue('/home/receiver/path' in settings.get_receiver_path())
        self.assertTrue('test/producer_sim/path' in settings.get_producer_sim_path())
        settings.delete_converter_path('C:\\\\test\\\\converter\\\\path')
        settings.delete_receiver_path('/home/receiver/path')
        settings.delete_producer_sim_path('test/producer_sim/path')
        self.assertFalse('C:\\\\test\\\\converter\\\\path' in settings.get_converter_path())
        self.assertFalse('/home/receiver/path' in settings.get_receiver_path())
        self.assertFalse('test/producer_sim/path' in settings.get_producer_sim_path())

    @unittest.skipIf(os.name == 'nt', 'This tests is only true on virtual linux x-server systems. Otherwise result value depends on test environment.')
    def test_interface_settings(self):
        self.assertTupleEqual(settings.get_window_geometry(), (100, 100, 1024, 768), 'This can fail if you started the online monitor once and changed the windows size')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSettings)
    unittest.TextTestRunner(verbosity=2).run(suite)