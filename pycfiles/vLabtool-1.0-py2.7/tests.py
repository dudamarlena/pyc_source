# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/tests/tests.py
# Compiled at: 2015-06-20 06:13:25
import unittest

class TestUnit(unittest.TestCase):

    def setUp(self):
        import Labtools
        print 'import successful'

    def test_voltage_read(self):
        import Labtools.interface as i
        I = i.Interface()
        print self.I.get_average_voltage('CH1')


if __name__ == '__main__':
    unittest.main()