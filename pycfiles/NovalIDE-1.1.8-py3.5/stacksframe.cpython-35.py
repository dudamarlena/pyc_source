# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/debugger/stacksframe.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 8211 bytes
from noval import GetApp, _, NewId
import noval.iface as iface, noval.plugin as plugin
from tkinter import ttk
import tkinter as tk, noval.ttkwidgets.treeviewframe as treeviewframe, noval.python.debugger.watchs as watchs, noval.menu as tkmenu, noval.constants as constants, noval.util.utils as utils, bz2
from xml.dom.minidom import parseString
import noval.consts as consts
from noval.python.debugger.commandui import BaseDebuggerUI

class StackFrameTab(ttk.Frame, watchs.CommonWatcher):
    __doc__ = 'description of class'
    AddWatchId = NewId()
    toInteractID = NewId()

    def __init__(self, parent, **tree_kw):
        ttk.Frame.__init__(self, parent)
        row = ttk.Frame(self)
        ttk.Label(row, text=_('Stack Frame:')).pack(fill='x', side=tk.LEFT)
        self.frameValue = tk.StringVar()
        self._framesChoiceCtrl = ttk.Combobox(row, textvariable=self.frameValue)
        self._framesChoiceCtrl.state(['readonly'])
        self._framesChoiceCtrl.pack(fill='x', side=tk.LEFT, expand=1)
        row.pack(fill='x')
        self._framesChoiceCtrl.bind('<<ComboboxSelected>>', self.ListItemSelected)
        row = ttk.Frame(self)
        self.treeview = treeviewframe.TreeViewFrame(row, columns=['Value', 'Hide'], displaycolumns=0)
        self.tree = self.treeview.tree
        self.tree.heading('#0', text='Thing', anchor=tk.W)
        self.tree.heading('Value', text='Value', anchor=tk.W)
        self.tree.column('#0', width=60, anchor='w')
        self.tree['show'] = ('headings', 'tree')
        self.treeview.pack(fill='both', expand=1)
        row.pack(fill='both', expand=1)
        self._root = self.tree.insert('', 'end', text='Frame')
        self.tree.bind('<<TreeviewOpen>>', self.IntrospectCallback)
        self.tree.bind('<3>', self.OnRightClick, True)
        self.menu = None

    def ListItemSelected(self, event):
        self.PopulateTreeFromFrameMessage(self.frameValue.get())
        self.OnSyncFrame()

    def OnRightClick(self, event):
        if not self.tree.selection() or not BaseDebuggerUI.DebuggerRunning():
            return
        self._introspectItem = self.tree.selection()[0]
        if self._introspectItem == self._root:
            return
        self._parentChain = self.GetItemChain(self._introspectItem)
        watchOnly = len(self._parentChain) < 1
        if self.menu is None:
            self.menu = tkmenu.PopupMenu()
            item = tkmenu.MenuItem(constants.ID_ADD_WATCH, _('Add a Watch'), None, watchs.getAddWatchBitmap(), None)
            self.menu.AppendMenuItem(item, handler=self.OnAddWatch)
            item = tkmenu.MenuItem(self.AddWatchId, _('Add to Watch'), None, watchs.getAddtoWatchBitmap(), None)
            self.menu.AppendMenuItem(item, handler=self.OnAddToWatch)
            item = tkmenu.MenuItem(watchs.WatchsPanel.ID_VIEW_WATCH, _('View in Dialog'), None, None, None)
            self.menu.AppendMenuItem(item, handler=self.OnView)
            item = tkmenu.MenuItem(self.toInteractID, _('Send to Interact'), None, None, None)
            self.menu.AppendMenuItem(item, handler=self.OnSendToInteract)
        self.menu.tk_popup(event.x_root, event.y_root)

    def OnAddWatch(self):
        GetApp().GetDebugger()._debugger_ui.OnAddWatch()

    def OnAddToWatch(self):
        name = self.tree.item(self._introspectItem, 'text')
        GetApp().GetDebugger()._debugger_ui.framesTab.AddtoWatchExpression(name, name)

    def OnSendToInteract(self):
        """
            执行右键菜单发送到交互命令
        """
        value = ''
        prevItem = ''
        for item in self._parentChain:
            if item.find(prevItem + '[') != -1:
                value += item[item.find('['):]
                continue
                if value != '':
                    value = value + '.'
                if item == 'globals':
                    item = 'globals()'
                if item != 'locals':
                    value += item
                    prevItem = item

        utils.get_logger().debug('send command is:%s', value)
        GetApp().GetDebugger()._debugger_ui.framesTab.ExecuteCommand(value)

    def OnView(self):
        self.ViewExpression(self._introspectItem)

    def DeleteChildren(self, item):
        for child in self.tree.get_children(item):
            self.tree.delete(child)

    def IntrospectCallback(self, event):
        """
            展开节点时实时获取节点的所有子节点的值
        """
        item = self.tree.selection()[0]
        if item == self._root:
            return
        watchs.CommonWatcher.IntrospectCallback(self)

    def GetFrameNode(self):
        return self._stack[int(self.currentItem)]

    def PopulateTreeFromFrameNode(self, frameNode):
        self._framesChoiceCtrl['state'] = 'readonly'
        tree = self.tree
        root = self._root
        self.DeleteChildren(root)
        children = frameNode.childNodes
        firstChild = None
        for index in range(0, children.length):
            subNode = children.item(index)
            treeNode = self.AppendSubTreeFromNode(subNode, subNode.getAttribute('name'), root)
            if not firstChild:
                firstChild = treeNode

        tree.item(root, open=True)
        if firstChild:
            tree.item(firstChild, open=True)

    def LoadFrame(self, domDoc):
        nodeList = domDoc.getElementsByTagName('frame')
        frame_count = -1
        frame_values = []
        self._stack = []
        for index in range(0, nodeList.length):
            frameNode = nodeList.item(index)
            message = frameNode.getAttribute('message')
            frame_values.append(message)
            self._stack.append(frameNode)
            frame_count += 1

        index = len(self._stack) - 1
        self._framesChoiceCtrl['values'] = frame_values
        self._framesChoiceCtrl.current(index)
        node = self._stack[index]
        self.currentItem = index
        self.PopulateTreeFromFrameNode(node)
        self.OnSyncFrame()
        frameNode = nodeList.item(index)
        file = frameNode.getAttribute('file')
        line = frameNode.getAttribute('line')
        GetApp().GetDebugger()._debugger_ui.framesTab.SynchCurrentLine(file, line)

    def OnSyncFrame(self):
        """
            定位到当前断点调试所在的文件行
        """
        frameNode = self._stack[int(self.currentItem)]
        file = frameNode.getAttribute('file')
        line = frameNode.getAttribute('line')
        GetApp().GetDebugger()._debugger_ui.framesTab.SynchCurrentLine(file, line)

    def PopulateTreeFromFrameMessage(self, message):
        index = 0
        for node in self._stack:
            if node.getAttribute('message') == message:
                binType = GetApp().GetDebugger()._debugger_ui.framesTab.request_frame_document(message)
                xmldoc = bz2.decompress(binType.data)
                domDoc = parseString(xmldoc)
                nodeList = domDoc.getElementsByTagName('frame')
                self.currentItem = index
                if len(nodeList):
                    self.PopulateTreeFromFrameNode(nodeList[0])
                return
            index = index + 1

    def HasStack(self):
        return hasattr(self, '_stack')

    def GetWatchList(self, watch_obj):
        """
            从断点调试服务器中获取监视的值
        """
        frameNode = self._stack[int(self.currentItem)]
        message = frameNode.getAttribute('message')
        binType = GetApp().GetDebugger()._debugger_ui.framesTab.add_watch(message, watch_obj)
        xmldoc = bz2.decompress(binType.data)
        domDoc = parseString(xmldoc)
        nodeList = domDoc.getElementsByTagName('watch')
        return nodeList


class StackframeViewLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        GetApp().MainFrame.AddView(consts.STACKFRAME_TAB_NAME, StackFrameTab, _('Stack Frame'), 'se', image_file='python/debugger/flag.ico')