# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_check/test_uuids.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1983 bytes
import unittest
from fluentcheck.classes import Check
from fluentcheck.exceptions import CheckError

class TestUUIDSAssertions(unittest.TestCase):

    def test_is_uuid1(self):
        res = Check('5245eb82-31e6-11e9-8bfa-d8cb8a1a56c7').is_uuid1()
        self.assertIsInstance(res, Check)
        try:
            Check('9f9b0fc0-e3bb-43af-9894-7b73c83374d1').is_uuid1()
            self.fail()
        except CheckError:
            pass

        try:
            Check('fluent').is_uuid1()
            self.fail()
        except CheckError:
            pass

    def test_is_not_uuid1(self):
        res = Check('9f9b0fc0-e3bb-43af-9894-7b73c83374d1').is_not_uuid1()
        self.assertIsInstance(res, Check)
        try:
            Check('fluent').is_not_uuid1()
            self.fail()
        except:
            pass

        try:
            Check('9194da68-31e8-11e9-8677-d8cb8a1a56c7').is_not_uuid1()
            self.fail()
        except CheckError:
            pass

    def test_is_uuid4(self):
        res = Check('80d2fde3-dc11-4e0c-a23d-3ebbfb203681').is_uuid4()
        self.assertIsInstance(res, Check)
        try:
            Check('e3cad24c-31e7-11e9-8936-d8cb8a1a56c7').is_uuid4()
            self.fail()
        except CheckError:
            pass

        try:
            Check('fluent').is_uuid4()
            self.fail()
        except CheckError:
            pass

    def test_is_not_uuid4(self):
        res = Check('f2b7a812-31e8-11e9-898b-d8cb8a1a56c7').is_not_uuid4()
        self.assertIsInstance(res, Check)
        try:
            Check('fluent').is_not_uuid4()
            self.fail()
        except:
            pass

        try:
            Check('725655d0-9840-4aec-9e3e-83e707dfa37c').is_not_uuid4()
            self.fail()
        except CheckError:
            pass