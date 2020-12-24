# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\lib\items.py
# Compiled at: 2013-09-10 03:15:55
from __future__ import division, absolute_import, print_function, unicode_literals
from PySide import QtCore, QtGui

class Item(QtGui.QTreeWidgetItem):

    def __init__(self, parent, item_name, brief=None, summary=None):
        super(Item, self).__init__(parent)
        self.res = None
        self.parent = parent
        self.setText(0, item_name)
        self.setBrief(brief)
        self.setSummary(summary)
        return

    def setBrief(self, brief=None):
        self.setData(0, QtCore.Qt.UserRole, brief)

    def appendBrief(self, brief, once=False):
        if brief:
            brief_list = self.data(0, QtCore.Qt.UserRole)
            if not isinstance(brief_list, list):
                brief_list = [
                 brief_list]
            if not (once and brief in brief_list):
                brief_list.append(brief)
            self.setBrief(brief_list)

    def setSummary(self, summary=None):
        self.setData(1, QtCore.Qt.UserRole, summary)

    def setOk(self, message=None):
        self.appendBrief(message)
        self.setResult(0)

    def setWarning(self, message=None):
        self.appendBrief(message)
        self.setResult(-1)

    def setError(self, message=None):
        self.appendBrief(message)
        self.setResult(-2)

    def setResult(self, res=None):
        if res == None:
            return
        else:
            if self.res == None or self.res > res:
                self.res = res
                if res == 0:
                    self.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))
                elif res == -1:
                    self.setForeground(0, QtGui.QBrush(QtCore.Qt.darkYellow))
                elif res == -2:
                    self.setForeground(0, QtGui.QBrush(QtCore.Qt.red))
                if isinstance(self.parent, Item):
                    self.parent.setResult(res)
            return

    def set_style(self, style=b''):
        if b'B' in style:
            self.set_bold()
        if b'I' in style:
            self.set_italic()
        if b'D' in style:
            self.set_quiet()
        if b'E' in style:
            self.setExpanded(True)

    def set_bold(self):
        font = self.font(0)
        font.setBold(True)
        self.setFont(0, font)

    def set_italic(self):
        font = self.font(0)
        font.setItalic(True)
        self.setFont(0, font)

    def set_quiet(self):
        self.setForeground(0, QtGui.QBrush(QtCore.Qt.gray))


class DirItem(Item):

    def __init__(self, *args, **kargs):
        super(DirItem, self).__init__(*args, **kargs)
        self.set_bold()


class FileItem(Item):
    pass


class DisabledItem(Item):

    def __init__(self, *args, **kargs):
        super(DisabledItem, self).__init__(*args, **kargs)
        self.set_italic()