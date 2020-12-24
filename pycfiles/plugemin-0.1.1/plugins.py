# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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