# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/bat/errors/test_global_exception.py
# Compiled at: 2011-03-24 03:59:28
from chula.test import bat

class Test_global_exception(bat.Bat):

    def test_root(self):
        retval = self.request('/global_exception/index')
        self.assertTrue(retval.data.find('Application Error') >= 0)
        self.assertTrue(retval.data.find('variable_not_defined') >= 0)
        self.assertEquals(retval.status, 500)