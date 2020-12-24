# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plugboard/test/plugins.py
# Compiled at: 2006-02-14 14:34:53
from plugboard import plugin, engine
from zope import interface
import sys

class ITestPlugin(plugin.IPlugin):
    """
    Test
    """
    __module__ = __name__


class TestPlugin(plugin.Plugin):
    __module__ = __name__
    interface.implements(ITestPlugin)

    def __init__(self, application):
        try:
            self.dispatcher = engine.IEventDispatcher(self)
            self.dispatcher.add_event('test', (str, 'test data'))
        except:
            pass