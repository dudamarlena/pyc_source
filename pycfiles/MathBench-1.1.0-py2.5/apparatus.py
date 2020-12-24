# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/lab/apparatus.py
# Compiled at: 2008-02-07 14:10:42
"""
A slightly modified version of the filling widget from wx.py.
"""
import wx, wx.py.filling as filling, types

class ApparatusTree(filling.FillingTree):
    """
        Show the content of a given namespace and mkes it possible to
        filter out some elmements.
        """

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TR_DEFAULT_STYLE, rootObject=None, rootLabel=None, rootIsNamespace=False, static=False, show_private=False, expand_root=True):
        """
                Create the filling tree wit the same options as wx.py.FillingTree

                If show_private is False then do not show private (begining
                with '__') elements of the namespaces.
                """
        filling.FillingTree.__init__(self, parent, id, pos, size, style, rootObject, 'Apparatus', rootIsNamespace, static)
        self.show_private = show_private
        if expand_root:
            self.Expand(self.root)

    def addChildren(self, item):
        self.DeleteChildren(item)
        obj = self.GetPyData(item)
        children = self.objGetChildren(obj)
        if not children:
            return
        keys = children.keys()
        keys.sort(lambda x, y: cmp(str(x).lower(), str(y).lower()))
        for key in keys:
            itemtext = str(key)
            if not self.show_private and itemtext.startswith('__'):
                continue
            if type(obj) is types.DictType and type(key) is types.StringType and (item != self.root or item == self.root and not self.rootIsNamespace):
                itemtext = repr(key)
            child = children[key]
            data = wx.TreeItemData(child)
            branch = self.AppendItem(parent=item, text=itemtext, data=data)
            self.SetItemHasChildren(branch, self.objHasChildren(child))

    def OnItemActivated(self, event):
        """Launch a DirFrame."""
        item = event.GetItem()
        text = self.getFullName(item)
        obj = self.GetPyData(item)
        frame = filling.FillingFrame(parent=self, size=(600, 600), rootObject=obj, rootLabel=text, rootIsNamespace=False)
        frame.Show()

    def setText(self, txt):
        """
                Do nothing !
                """
        pass