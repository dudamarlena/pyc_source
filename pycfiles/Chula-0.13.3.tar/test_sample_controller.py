# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/bat/test_sample_controller.py
# Compiled at: 2011-03-19 21:05:04
from chula.test import bat
HTML = 'Sample controller'

class Test_sample_controller(bat.Bat):

    def test_root(self):
        retval = self.request('/sample')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_with_slash(self):
        retval = self.request('/sample/')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_method_specified(self):
        retval = self.request('/sample/page')
        self.assertEquals(retval.data, HTML + ':page')
        self.assertEquals(retval.status, 200)

    def test_method_specified_with_slash(self):
        retval = self.request('/sample/page/')
        self.assertEquals(retval.data, HTML + ':page')
        self.assertEquals(retval.status, 200)