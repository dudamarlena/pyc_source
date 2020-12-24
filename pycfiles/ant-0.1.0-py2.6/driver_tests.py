# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ant/core/tests/driver_tests.py
# Compiled at: 2011-10-07 13:52:23
import unittest
from ant.core.driver import *

class DummyDriver(Driver):

    def _open(self):
        pass

    def _close(self):
        pass

    def _read(self, count):
        return '\x00' * count

    def _write(self, data):
        return len(data)


class DriverTest(unittest.TestCase):

    def setUp(self):
        self.driver = DummyDriver('superdrive')

    def tearDown(self):
        pass

    def test_isOpen(self):
        self.assertFalse(self.driver.isOpen())
        self.driver.open()
        self.assertTrue(self.driver.isOpen())
        self.driver.close()
        self.assertFalse(self.driver.isOpen())

    def test_open(self):
        self.driver.open()
        self.assertRaises(DriverError, self.driver.open)
        self.driver.close()

    def test_close(self):
        pass

    def test_read(self):
        self.assertFalse(self.driver.isOpen())
        self.assertRaises(DriverError, self.driver.read, 1)
        self.driver.open()
        self.assertEqual(len(self.driver.read(5)), 5)
        self.assertRaises(DriverError, self.driver.read, -1)
        self.assertRaises(DriverError, self.driver.read, 0)
        self.driver.close()

    def test_write(self):
        self.assertRaises(DriverError, self.driver.write, b'\xff')
        self.driver.open()
        self.assertRaises(DriverError, self.driver.write, '')
        self.assertEquals(self.driver.write(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'), 10)
        self.driver.close()


class USB1DriverTest(unittest.TestCase):

    def _open(self):
        pass

    def _close(self):
        pass

    def _read(self):
        pass

    def _write(self):
        pass