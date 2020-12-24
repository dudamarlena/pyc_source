# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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