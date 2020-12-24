# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_raises_exception.py
# Compiled at: 2013-08-11 10:36:51
import sys, suds, unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class RaisesExceptionTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_simple(self):
        try:
            self.service.raises_exception('hello')
        except suds.WebFault as e:
            self.assertEqual(e.fault.faultstring, 'hello error')
            return

        self.assertTrue(False, "Exception hasn't been thrown")

    @unittest.skipIf(sys.version_info[1] == 5, 'suds does not handle unicode in faultstrings properly on python 2.5')
    def test_unicode(self):
        try:
            self.service.raises_exception('лопата')
        except suds.WebFault as e:
            self.assertEqual(e.fault.faultstring, 'лопата error')
            return

        self.assertTrue(False, "Exception hasn't been thrown")