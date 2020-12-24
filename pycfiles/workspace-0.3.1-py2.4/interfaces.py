# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.5.0-Power_Macintosh/egg/workspace/interfaces.py
# Compiled at: 2006-04-01 12:02:41
from zope.interface import Interface, Attribute, implements
from sprinkles import ISprinkle

class IWorkspaceSection(ISprinkle):
    __module__ = __name__
    name = Attribute('the section name')

    def append(self, l):
        """parse in a new line"""
        pass

    def canHandle(cls, name):
        """ called to see if this sction handles the given section heading """
        pass


class IWorkspaceCommand(ISprinkle):
    __module__ = __name__

    def canHandle(cls, cmd):
        """ called to check whether the given parser can handle the stuffs"""
        pass

    def handle(self, args):
        """ executes the given command """
        pass