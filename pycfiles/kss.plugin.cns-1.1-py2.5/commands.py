# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/kss/plugin/cns/commands/commands.py
# Compiled at: 2008-12-14 04:09:28
from zope.interface import implements
from kss.core import CommandSet
from interfaces import ICNSCommands

class CNSCommands(CommandSet):
    implements(ICNSCommands)

    def redirectRequest(self, url=''):
        """ see interfaces.py """
        command = self.commands.addCommand('redirectRequest')
        data = command.addParam('url', url)

    def valueSetter(self, target_element, source_element=None, value=None, attribute=None, condition_element=None, condition_attribute=None, condition_value=None):
        command = self.commands.addCommand('valueSetter')
        command.addParam('target_element', target_element)
        if source_element is not None:
            command.addParam('source_element', source_element)
        if value is not None:
            command.addParam('value', value)
        if attribute is not None:
            command.addParam('attribute', attribute)
        if condition_element is not None:
            command.addParam('condition_element', condition_element)
        if condition_attribute is not None:
            command.addParam('condition_attribute', condition_attribute)
        if condition_value is not None:
            command.addParam('condition_value', condition_value)
        return

    def alertText(self, message):
        command = self.commands.addCommand('alertText')
        command.addParam('message', message)

    def openWindow(self, url):
        command = self.commands.addCommand('openWindow')
        command.addParam('url', url)

    def removeAttribute(self, selector, name):
        command = self.commands.addCommand('removeAttribute', selector)
        command.addParam('name', name)