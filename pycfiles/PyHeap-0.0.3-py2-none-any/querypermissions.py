# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/querypermissions.py
# Compiled at: 2015-12-13 13:38:41
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.querypermissions import QueryPermissions

class TestQueryPermissions(TestBase):

    def test_querypermissions(self):
        itemtypes = [
         '822a5e5a-14f1-4d06-b92f-8f3f1b05218f',
         'a5033c9d-08cf-4204-9bd3-cb412ce39fc0',
         '40750a6a-89b2-455c-bd8d-b420a4cb500b']
        method = QueryPermissions(itemtypes)
        method.execute(conn)
        for i in method.response.permissions:
            self.assertIn(i.thing_type_id, itemtypes)
            self.assertTrue(i.offline_access_permissions != 0 or i.online_access_permissions != 0)