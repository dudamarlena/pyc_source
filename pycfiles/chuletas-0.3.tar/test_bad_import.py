# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/bat/errors/test_bad_import.py
# Compiled at: 2011-03-24 03:59:28
from chula.test import bat

class Test_bad_import(bat.Bat):

    def test_root(self):
        retval = self.request('/bad_import/index')
        self.assertTrue(retval.data.find('Application Error') >= 0)
        self.assertTrue(retval.data.find('intentionally') >= 0, retval.data)
        self.assertEquals(retval.status, 500)