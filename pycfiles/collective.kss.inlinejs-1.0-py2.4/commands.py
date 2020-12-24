# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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