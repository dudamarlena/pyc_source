# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_getauthorizedpeople.py
# Compiled at: 2015-12-19 03:57:52
import pytz
from datetime import datetime
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.getauthorizedpeople import GetAuthorizedPeople
from healthvaultlib.objects.getauthorizedpeopleparameters import GetAuthorizedPeopleParameters

class TestGetAuthorizedPeople(TestBase):

    def test_getauthroizedpeople(self):
        method = GetAuthorizedPeople(GetAuthorizedPeopleParameters())
        method.execute(self.connection)
        response = method.response
        self.assertNotEqual(len(response.authorized_people), 0)
        self.assertIsNotNone(response.authorized_people[0].name)
        self.assertNotEqual(len(response.authorized_people[0].records), 0)

    def test_getauthroizedpeople_with_since(self):
        params = GetAuthorizedPeopleParameters()
        params.authorizations_created_since = datetime.now(pytz.utc)
        method = GetAuthorizedPeople(params)
        method.execute(self.connection)
        response = method.response
        self.assertIsNotNone(response)
        self.assertEqual(len(response.authorized_people), 0)

    def test_getauthroizedpeople_with_num(self):
        params = GetAuthorizedPeopleParameters()
        params.num_results = 1
        method = GetAuthorizedPeople(params)
        method.execute(self.connection)
        response = method.response
        self.assertIsNotNone(response)
        self.assertEqual(len(response.authorized_people), 1)