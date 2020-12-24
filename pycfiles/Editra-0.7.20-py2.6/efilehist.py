# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/efilehist.py
# Compiled at: 2012-06-09 14:19:20
"""
Editra Business Model: EFileHistory

Enhanced File History - Provides more consistent behavior than wxFileHistory

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: efilehist.py 71668 2012-06-06 18:32:07Z CJP $'
__revision__ = '$Revision: 71668 $'
__all__ = [
 'EFileHistory']
import os, wx, txtutil

class EFileHistory(object):
    """FileHistory Menu Manager"""

    def __init__(self, maxFile=9):
        assert maxFile <= 9, 'supports at most 9 files'
        super(EFileHistory, self).__init__()
        self._history = list()
        self._maxFiles = maxFile
        self._menu = None
        return

    def _UpdateMenu(self):
        """Update the filehistory menu"""
        menu = self.Menu
        assert menu is not None
        for item in menu.GetMenuItems():
            menu.RemoveItem(item)

        to_remove = list()
        for item in self.History:
            if not item:
                to_remove.append(item)
            elif not os.path.exists(item):
                to_remove.append(item)

        for item in to_remove:
            self.History.remove(item)

        for (index, histfile) in enumerate(self.History):
            menuid = wx.ID_FILE1 + index
            if menuid <= wx.ID_FILE9:
                menu.Append(menuid, histfile)
            else:
                break

        return

    Count = property(lambda self: self.GetCount())
    History = property(lambda self: self._history, lambda self, hist: self.SetHistory(hist))
    MaxFiles = property(lambda self: self._maxFiles)
    Menu = property(lambda self: self._menu, lambda self, menu: self.UseMenu(menu))

    def AddFileToHistory(self, fname):
        """Add a file to the history
        @param fname: Unicode

        """
        if not fname:
            return
        else:
            assert txtutil.IsUnicode(fname)
            assert self.Menu is not None
            if fname in self.History:
                self.History.remove(fname)
            self.History.insert(0, fname)
            if self.Count > self.MaxFiles:
                self._history.pop()
            self._UpdateMenu()
            return

    def GetCount(self):
        """Get the number of files in the history
        @return: int

        """
        return len(self._history)

    def GetHistoryFile(self, index):
        """Get the history file at the given index
        @param index: int
        @return: Unicode

        """
        assert self.MaxFiles > index, 'Index out of range'
        return self.History[index]

    def RemoveFileFromHistory(self, index):
        """Remove a file from the history"""
        assert self.MaxFiles > index, 'Index out of range'
        self.History.pop(index)
        self._UpdateMenu()

    def SetHistory(self, hist):
        """Set the file history from a list
        @param hist: list of Unicode

        """
        hist = list(set(hist))
        assert len(hist) <= self.MaxFiles
        self._history = hist
        self._UpdateMenu()

    def UseMenu(self, menu):
        """Set the menu for the file history to use
        @param menu: wx.Menu

        """
        assert isinstance(menu, wx.Menu)
        if self.Menu is not None:
            self._menu.Destroy()
        self._menu = menu
        self._UpdateMenu()
        return