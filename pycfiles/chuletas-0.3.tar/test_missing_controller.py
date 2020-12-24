# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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