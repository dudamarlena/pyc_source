# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_getapplicationinfo.py
# Compiled at: 2015-12-14 12:12:58
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.getapplicationinfo import GetApplicationInfo

class TestGetApplicationInfo(TestBase):

    def test_getapplicationinfo(self):
        method = GetApplicationInfo(True)
        method.execute(self.connection)
        response = method.response
        self.assertIsNotNone(response)