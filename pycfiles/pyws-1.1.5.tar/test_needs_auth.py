# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_needs_auth.py
# Compiled at: 2013-09-14 14:25:32
import suds, unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class RaisesExceptionTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_simple(self):
        headers = self.factory.create('types:Headers')
        headers.username = 'user'
        headers.password = 'pass'
        self.client.set_options(soapheaders=headers)
        self.assertEqual(self.service.say_hello(), 'hello user')

    def _test_exception(self, message):
        try:
            self.service.say_hello()
        except suds.WebFault as e:
            self.assertEqual(e.fault.faultstring, message)
            return

        self.assertTrue(False, "Exception hasn't been thrown")

    def test_none_exception(self):
        self._test_exception('Access denied')

    def test_exception(self):
        headers = self.factory.create('types:Headers')
        headers.username = 'fake'
        headers.password = 'pass'
        self.client.set_options(soapheaders=headers)
        self._test_exception('Access denied for user fake')