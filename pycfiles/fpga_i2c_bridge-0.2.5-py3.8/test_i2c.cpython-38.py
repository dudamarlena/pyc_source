# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/test/test_i2c.py
# Compiled at: 2020-04-09 04:36:36
# Size of source mod 2**32: 930 bytes
from unittest import TestCase
from fpga_i2c_bridge import I2CBridge, I2CApplianceType, I2CSensorType

class TestI2C(TestCase):
    APPLIANCES = [
     4, 3, 2, 1]
    SENSORS = [2, 3, 1, 4, 5]
    VERSION = 57005

    def setUp(self) -> None:
        self.i2c = I2CBridge(i2c_dummy=True, i2c_dummy_appliances=(self.APPLIANCES), i2c_dummy_sensors=(self.SENSORS))

    def test_get_devices(self):
        self.assertEqual(len(self.i2c.appliances), len(self.APPLIANCES))
        self.assertEqual(len(self.i2c.sensors), len(self.SENSORS))
        for i, dev_type in enumerate(self.APPLIANCES):
            self.assertEqual(self.i2c.appliances[i].device_type, I2CApplianceType(dev_type))
        else:
            for i, dev_type in enumerate(self.SENSORS):
                self.assertEqual(self.i2c.sensors[i].sensor_type, I2CSensorType(dev_type))

    def test_version(self):
        self.assertEqual(self.i2c.version, self.VERSION)