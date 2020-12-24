# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/test/plugins/plugin_test_1.py
# Compiled at: 2009-01-30 08:10:10
from zope.interface import implements
from twisted.plugin import IPlugin
from spamfighter.test.plugins import ITestPlugin1

class TestPlugin1(object):
    implements(IPlugin, ITestPlugin1)

    def name(self):
        return 'testplugin1'


plugin1 = TestPlugin1()