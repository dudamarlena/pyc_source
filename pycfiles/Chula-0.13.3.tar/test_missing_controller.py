# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/bat/errors/test_missing_controller.py
# Compiled at: 2011-03-24 03:59:28
from chula.test import bat
HTML = '<h1>404</h1>'

class Test_missing_controller(bat.Bat):

    def test_root(self):
        retval = self.request('/missing_controller')
        self.assertTrue(HTML in retval.data, retval.data)
        self.assertEquals(retval.status, 404)

    def test_root_with_slash(self):
        retval = self.request('/missing_controller/')
        self.assertTrue(HTML in retval.data, retval.data)
        self.assertEquals(retval.status, 404)

    def test_method_specified(self):
        retval = self.request('/missing_controller/foobar')
        self.assertTrue(HTML in retval.data, retval.data)
        self.assertEquals(retval.status, 404)

    def test_package_method_specified(self):
        retval = self.request('/foopackage/foocontroller/foomethod')
        self.assertTrue(HTML in retval.data, retval.data)
        self.assertEquals(retval.status, 404)

    def test_deep_package_method_specified(self):
        retval = self.request('/foo/bar/black/red/blue/green/white')
        self.assertTrue(HTML in retval.data, retval.data)
        self.assertEquals(retval.status, 404)