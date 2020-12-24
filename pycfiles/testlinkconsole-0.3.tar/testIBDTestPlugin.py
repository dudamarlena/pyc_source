# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/tests/libs/testIBDTestPlugin.py
# Compiled at: 2014-07-07 11:11:13
import unittest, mock
from libs.iBDTestPlugin import IBDTestPlugin

class TestIBDTestPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = IBDTestPlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), 'IBDTestPlugin actif')

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), 'IBDTestPlugin inactif')