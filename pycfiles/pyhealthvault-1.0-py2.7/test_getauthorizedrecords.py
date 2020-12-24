# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_getauthorizedrecords.py
# Compiled at: 2016-01-06 13:11:26
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.getauthorizedrecords import GetAuthorizedRecords

class TestGetAuthorizedRecords(TestBase):

    def test_getauthroizedrecords(self):
        method = GetAuthorizedRecords([self.connection.recordid,
         self.connection.personid])
        method.execute(self.connection)
        response = method.response
        self.assertEqual(len(response.records), 1)
        self.assertIsNotNone(response.records[0].id)
        self.assertEqual(response.records[0].id, self.connection.recordid)