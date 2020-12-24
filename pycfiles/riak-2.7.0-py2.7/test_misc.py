# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_misc.py
# Compiled at: 2016-10-17 19:06:50
import unittest

class MiscTests(unittest.TestCase):

    def test_timeout_validation(self):
        from riak.client.operations import _validate_timeout
        try:
            _validate_timeout(None)
            _validate_timeout(None, infinity_ok=True)
            _validate_timeout('infinity', infinity_ok=True)
            _validate_timeout(1234)
            _validate_timeout(1234567898765432123456789)
        except ValueError:
            self.fail('_validate_timeout() unexpectedly raised ValueError')

        with self.assertRaises(ValueError):
            _validate_timeout('infinity')
        with self.assertRaises(ValueError):
            _validate_timeout('infinity-foo')
        with self.assertRaises(ValueError):
            _validate_timeout('foobarbaz')
        with self.assertRaises(ValueError):
            _validate_timeout('1234')
        with self.assertRaises(ValueError):
            _validate_timeout(0)
        with self.assertRaises(ValueError):
            _validate_timeout(12.34)
        return