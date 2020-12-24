# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\tests\basic\test_dijit.py
# Compiled at: 2013-06-05 06:34:59
from base import BasicTestCase
import pyojo.js as js, pyojo.js.dojo as dojo, pyojo.js.dijit as dijit

class TestDijit(BasicTestCase):

    def setUp(self):
        self.x = dijit.Dijit()

    def test_class(self):
        self.assertIsInstance(self.x, js.Code)
        self.assertIsInstance(self.x, dojo.Dojo)
        self.assertIsInstance(self.x, dijit.Dijit)
        assert str(type(self.x)) == "<class 'pyojo.js.dijit.base.Dijit'>"
        print js.get_code(self.x)