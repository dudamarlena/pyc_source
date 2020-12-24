# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/data/test_value.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1121 bytes
import time, unittest
from drove.data.value import Value

class TestValue(unittest.TestCase):

    def test_value(self):
        """Testing Value: dump()"""
        value = Value('example', 42, nodename='test', timestamp=0)
        assert value.is_value()
        assert value.dump() == 'V|0|test|example|42.0|g'
        value = Value('example', 42, nodename='test')
        assert value.dump() == 'V|%d|test|example|42.0|g' % (int(time.time()),)
        assert value.value_id == 'test.example'

    def test_value_dump(self):
        """Testing Value: from_dump()"""
        value = Value.from_dump('V|0|test|example|42.0|g')
        assert value.dump() == 'V|0|test|example|42.0|g' == repr(value)

    def test_value_malformed(self):
        """Testing Value: malformed event"""
        with self.assertRaises(ValueError):
            Value.from_dump('E|0')

    def test_value_invalid_type(self):
        """Testing Value: invalid value type"""
        with self.assertRaises(ValueError):
            Value.from_dump('V|0|test|example|42.0|ZZ')