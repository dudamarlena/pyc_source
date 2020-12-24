# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/test/plugins/plugin_test_2.py
# Compiled at: 2009-01-30 08:10:10
from zope.interface import implements
from twisted.plugin import IPlugin
from spamfighter.test.plugins import ITestPlugin1, ITestPlugin2

class TestPlugin2(object):
    implements(IPlugin, ITestPlugin1, ITestPlugin2)

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name


plugin1 = TestPlugin2('testplugin2')
plugin2 = TestPlugin2('testplugin3')
plugin3 = TestPlugin2('testplugin3')