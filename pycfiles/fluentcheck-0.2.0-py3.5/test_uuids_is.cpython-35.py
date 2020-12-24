# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_uuids_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 2127 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError

class TestIsUUIDSAssertions(unittest.TestCase):

    def test_is_uuid1_pass(self):
        obj = '5245eb82-31e6-11e9-8bfa-d8cb8a1a56c7'
        self.assertIsInstance(Is(obj).uuid1, Is)

    def test_is_uuid1_fail(self):
        obj = '9f9b0fc0-e3bb-43af-9894-7b73c83374d1'
        with self.assertRaises(CheckError):
            Is(obj).uuid1
        with self.assertRaises(CheckError):
            Is('fluent').uuid1

    def test_is_not_uuid1_pass(self):
        obj = '9f9b0fc0-e3bb-43af-9894-7b73c83374d1'
        self.assertIsInstance(Is(obj).not_uuid1, Is)

    def test_is_not_uuid1_fail(self):
        obj = '5245eb82-31e6-11e9-8bfa-d8cb8a1a56c7'
        with self.assertRaises(CheckError):
            Is(obj).not_uuid1

    def test_is_uuid4_pass(self):
        obj = '9f9b0fc0-e3bb-43af-9894-7b73c83374d1'
        self.assertIsInstance(Is(obj).uuid4, Is)

    def test_is_uuid4_fail(self):
        obj = '5245eb82-31e6-11e9-8bfa-d8cb8a1a56c7'
        with self.assertRaises(CheckError):
            Is(obj).uuid4
        with self.assertRaises(CheckError):
            Is('fluent').uuid4

    def test_is_not_uuid4_pass(self):
        obj = '5245eb82-31e6-11e9-8bfa-d8cb8a1a56c7'
        self.assertIsInstance(Is(obj).not_uuid4, Is)

    def test_is_not_uuid4_fail(self):
        obj = '9f9b0fc0-e3bb-43af-9894-7b73c83374d1'
        with self.assertRaises(CheckError):
            Is(obj).not_uuid4