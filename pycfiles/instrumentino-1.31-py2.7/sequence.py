# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/sequence.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
__author__ = 'yoelk'
import wx
from wx import xrc
import copy, sys, wx.lib.filebrowsebutton as filebrowse, wx.lib.masked as masked
from instrumentino import cfg
import pickle
from executable_listctrl import ExecutableListCtrl
from method import SysMethod

class MethodsListCtrl(ExecutableListCtrl):
    """
    A list of methods to be run
    """

    def __init__(self, parent, methods=[]):
        ExecutableListCtrl.__init__(self, parent, xrc.XRCCTRL(parent, 'methodsListPanel'), {1: 'Method', 2: 'Repeat'}, '=== run sequence ===', methods)

    def getDefaultDataItem(self):
        """
        Return an empty method item
        """
        return SysMethod()

    def getFirstColumnWidget(self, panel, listDataItem):
        """
        Return the widget for the first column (a file dialog in this case)
        """
        fileBrowser = filebrowse.FileBrowseButton(panel, labelText='', dialogTitle='Choose a method file', startDirectory=cfg.UserFilesPath(), fileMask=cfg.methodWildcard, fileMode=wx.OPEN, changeCallback=listDataItem.onPathChanged)
        filename = listDataItem.methodFileName
        if not listDataItem.checkSystemCompatibility(filename):
            filename = ''
        fileBrowser.SetValue(filename)
        return fileBrowser

    def setOtherColumns(self, index, listDataItem):
        """
        Set the other columns' content
        """
        item = self.list.GetItem(index, self.columnNameToNum['Repeat'])
        item.SetWindow(listDataItem.setRepeatPanel(self.list), expand=True)
        self.list.SetItem(item)