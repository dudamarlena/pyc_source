# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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