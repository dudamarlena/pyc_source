# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/test/test_plugin.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.plugin}.
"""
import unittest
from spamfighter import plugin
from spamfighter.test.plugins import ITestPlugin1, ITestPlugin2, ITestPlugin3
import spamfighter.test.plugins

class PluginTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.plugin.loadPlugin}.
    """

    def testLoadPlugin(self):
        plug1 = plugin.loadPlugin(ITestPlugin1, 'testplugin1', spamfighter.test.plugins)
        self.assert_(ITestPlugin1.providedBy(plug1))
        self.assertEqual('testplugin1', plug1.name())
        plug2 = plugin.loadPlugin(ITestPlugin1, 'testplugin2', spamfighter.test.plugins)
        self.assert_(ITestPlugin1.providedBy(plug2))
        self.assert_(ITestPlugin2.providedBy(plug2))
        self.assertEqual('testplugin2', plug2.name())

    def testLoadPluginNotFound(self):
        self.assertRaises(plugin.PluginNotFoundError, plugin.loadPlugin, ITestPlugin1, 'testplugin45', spamfighter.test.plugins)
        self.assertRaises(plugin.PluginNotFoundError, plugin.loadPlugin, ITestPlugin3, 'testplugin1', spamfighter.test.plugins)

    def testLoadPluginAmbiguity(self):
        self.assertRaises(plugin.PluginAmbiguityError, plugin.loadPlugin, ITestPlugin2, 'testplugin3', spamfighter.test.plugins)