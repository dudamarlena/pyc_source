# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/testbase.py
# Compiled at: 2015-12-13 13:27:03
import unittest, settings
from healthvaultlib.helpers.connection import Connection

class TestBase(unittest.TestCase):

    def setUp(self):
        self.connection = self.get_connection()

    def get_connection(self):
        conn = Connection(settings.HV_APPID, settings.HV_SERVICE_SERVER)
        conn.thumbprint = settings.APP_THUMBPRINT
        conn.publickey = settings.APP_PUBLIC_KEY
        conn.privatekey = settings.APP_PRIVATE_KEY
        conn.connect()
        conn.set_person_and_record(settings.OFFLINE_PERSON_ID, settings.OFFLINE_RECORD_ID)
        return conn