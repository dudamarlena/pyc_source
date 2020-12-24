# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/LiveChat/kss/LiveChatKSSCommands.py
# Compiled at: 2008-07-25 11:17:39
from qi.LiveChat.kss.ILiveChatKSSCommands import ILiveChatKSSCommands
from kss.core import CommandSet
from zope import interface

class LiveChatKSSCommands(CommandSet):
    __module__ = __name__
    interface.implements(ILiveChatKSSCommands)

    def resetScrollbar(self, selector):
        command = self.commands.addCommand('resetScrollbar', selector)

    def resetInput(self, selector):
        command = self.commands.addCommand('resetInput', selector)