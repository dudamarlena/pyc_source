# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/Sensor_test.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 1040 bytes
import unittest
from Goap.Sensor import Sensors

class SensorsTest(unittest.TestCase):

    def setUp(self):
        self.sensors = Sensors()

    def test_add_success(self):
        self.sensors = Sensors()
        self.sensors.add(name='SenseTmpDirState',
          shell='if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi',
          binding='tmp_dir_state')
        self.sensors.add(name='SenseTmpDirContent',
          shell='[ -f /tmp/goap_tmp/.token ] && echo -n "token_found" || echo -n "token_not_found"',
          binding='tmp_dir_content')
        assert 'SenseTmpDirState' == str(self.sensors.get(name='SenseTmpDirState'))
        assert 'SenseTmpDirContent' == str(self.sensors.get(name='SenseTmpDirContent'))

    def test_remove_sensor_success(self):
        assert self.sensors.remove(name='SenseTmpDirContent') is True

    def test_remove_sensor_error(self):
        assert self.sensors.remove(name='CreateAPP') is False