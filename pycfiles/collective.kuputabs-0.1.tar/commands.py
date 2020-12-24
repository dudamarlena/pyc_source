# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/inlinejs/commands.py
# Compiled at: 2009-05-29 04:51:52
from zope.interface import implements
from kss.core.kssview import CommandSet
from collective.kss.inlinejs.interfaces import IInlineJsCommands

class InlineJsCommands(CommandSet):
    __module__ = __name__
    implements(IInlineJsCommands)
    effect = 'inlinejs-effect'

    def execJs(self, selector, code, debug='0'):
        command = self.commands.addCommand(self.effect, selector)
        command.addParam('code', code)
        command.addParam('debug', debug)