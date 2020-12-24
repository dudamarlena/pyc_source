# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/kss/GobanKSSCommands.py
# Compiled at: 2008-04-06 04:02:01
from qi.Goban.kss.IGobanKSSCommands import IGobanKSSCommands
from kss.core import CommandSet
from zope import interface

class GobanKSSCommands(CommandSet):
    __module__ = __name__
    interface.implements(IGobanKSSCommands)

    def setInputValue(self, selector, value):
        self.commands.addCommand('setInputValue', selector, newValue=value)