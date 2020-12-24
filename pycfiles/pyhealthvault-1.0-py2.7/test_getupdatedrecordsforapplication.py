# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_getupdatedrecordsforapplication.py
# Compiled at: 2016-01-06 14:02:12
import pytz
from datetime import datetime, timedelta
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.itemtypes.height import Height
from healthvaultlib.methods.putthings import PutThings
from healthvaultlib.methods.getupdatedrecordsforapplication import GetUpdatedRecordsForApplication

class TestGetUpdatedRecordsForApplication(TestBase):

    def test_getauthroizedrecords(self):
        personid = self.connection.personid
        self.connection.personid = None
        method = GetUpdatedRecordsForApplication()
        method.request.update_date = datetime.now(pytz.utc) + timedelta(days=3)
        method.execute(self.connection)
        response = method.response
        self.assertEqual(len(response.updated_records), 0)
        self.create_height_object(1.4, personid)
        method.request.update_date = datetime.now(pytz.utc)
        self.connection.personid = None
        method.execute(self.connection)
        response = method.response
        self.assertEqual(len(response.updated_records), 1)
        return

    def create_height_object(self, value_m, personid):
        self.connection.personid = personid
        height = Height()
        height.value_m = value_m
        height.display_value = str(value_m * 100)
        height.display_units = 'cm'
        method = PutThings([height])
        method.execute(self.connection)