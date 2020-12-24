# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.5.0-Power_Macintosh/egg/workspace/plugins/items_interfaces.py
# Compiled at: 2006-04-01 11:43:15
from zope.interface import Interface, Attribute
from sprinkles import ISprinkle

class IWorkspaceItem(ISprinkle):
    __module__ = __name__

    def fromSystem(cls):
        """ classmethod to return a list of workspace items """
        pass

    def serialize(self):
        """ returns a string that can be written to the workspace file """
        pass

    def unserialize(cls, s):
        """ classmethod to create an item from its serialized version """
        pass

    def load(self):
        """ should load the workspace item to the system """
        pass

    def __str__(self):
        """ string repr """
        pass