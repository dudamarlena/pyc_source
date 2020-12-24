# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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