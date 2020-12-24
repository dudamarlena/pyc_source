# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_newapplicationcreationinfo.py
# Compiled at: 2016-01-12 14:16:28
import unittest
from healthvaultlib.tests import settings
from healthvaultlib.helpers.connection import Connection
from healthvaultlib.exceptions.healthserviceexception import HealthServiceException
from healthvaultlib.methods.newapplicationcreationinfo import NewApplicationCreationInfo

class TestNewApplicationCreationInfo(unittest.TestCase):

    def setUp(self):
        self.connection = Connection(settings.SODA_MASTER_APPID, settings.HV_SERVICE_SERVER)

    def test_newapplicationcreationinfo(self):
        method = NewApplicationCreationInfo()
        method.execute(self.connection)
        response = method.response
        self.assertIsNotNone(response.app_id)
        self.assertIsNotNone(response.app_token)
        self.assertIsNotNone(response.shared_secret)

    def test_newapplicationcreationinfo_nonmaster(self):
        method = NewApplicationCreationInfo()
        self.connection.applicationid = settings.HV_APPID
        with self.assertRaises(HealthServiceException):
            method.execute(self.connection)