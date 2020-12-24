# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/tests/libs/testIRunnerPlugin.py
# Compiled at: 2014-07-07 11:09:18
import unittest, mock
from libs.iRunnerPlugin import IRunnerPlugin

class TestIRunnerPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = IRunnerPlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), 'IRunnerPlugin actif')

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), 'IRunnerPlugin inactif')