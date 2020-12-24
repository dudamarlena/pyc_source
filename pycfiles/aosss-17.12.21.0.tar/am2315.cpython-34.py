# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/matt/.pyenv/versions/3.4.1/lib/python3.4/site-packages/tests/am2315.py
# Compiled at: 2014-09-25 00:34:43
# Size of source mod 2**32: 1609 bytes
__doc__ = '\nCopyright 2014 Matt Heitzenroder\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
from aosong.am2315 import Sensor
import unittest, time

class TestSensor(unittest.TestCase):

    def setUp(self):
        self.sensor = Sensor()
        self.assertIn(self.sensor.channel, [0, 1])
        self.assertIs(self.sensor.address, 92)
        self.assertIsInstance(self.sensor, Sensor)
        self.assertIs(self.sensor.lastError, None)

    def test_pi_revision(self):
        self.assertIn(self.sensor.pi_revision(), [1, 2])

    def test_pi_i2c_bus_number(self):
        self.assertIn(self.sensor.pi_i2c_bus_number(), [0, 1])

    def test_data(self):
        time.sleep(0.5)
        data = self.sensor.data()
        self.assertIsNotNone(data)
        self.assertIs(len(data), 3)

    def test_humidity(self):
        time.sleep(0.5)
        self.assertIsNotNone(self.sensor.humidity())

    def test_temperature(self):
        time.sleep(0.5)
        self.assertIsNotNone(self.sensor.temperature())
        time.sleep(0.5)
        self.assertIsNotNone(self.sensor.temperature(False))