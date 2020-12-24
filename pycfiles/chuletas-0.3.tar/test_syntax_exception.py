# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/bat/errors/test_syntax_exception.py
# Compiled at: 2011-03-24 03:59:28
from chula.test import bat

class Test_syntax_exception(bat.Bat):

    def test_root(self):
        retval = self.request('/syntax_exception/index')
        self.assertTrue(retval.data.find('Application Error') >= 0)
        self.assertTrue(retval.data.find('invalid syntax') >= 0)
        self.assertTrue(retval.data.find('syntax_exception.py, line 5') >= 0)
        self.assertEquals(retval.status, 500)