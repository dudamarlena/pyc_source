# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/eclib/filemgrdlg.py
# Compiled at: 2010-02-02 23:05:14
"""
Editra Control Library: FileMgrDialog

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: filemgrdlg.py 63361 2010-02-03 04:03:45Z CJP $'
__revision__ = '$Revision: 63361 $'
__all__ = [
 'FileMgrDialog',
 'FMD_DEFAULT_STYLE', 'FMD_NO_DELETE']
import os, fnmatch, wx, wx.lib.mixins.listctrl as listmix, ecbasewin, elistmix
FMD_DEFAULT_STYLE = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
FMD_NO_DELETE = 1
_ = wx.GetTranslation

class FileMgrDialog(ecbasewin.ECBaseDlg):

    def __init__(self, parent, id=wx.ID_ANY, title='', defaultPath=os.curdir, defaultFile='', filter='*', pos=wx.DefaultPosition, size=wx.DefaultSize, style=FMD_DEFAULT_STYLE, name='FileMgrDialog'):
        ecbasewin.ECBaseDlg.__init__(self, parent, id, title, pos, size, style, name)
        panel = FileMgrPanel(self, defaultPath, defaultFile, filter)
        self.SetPanel(panel)
        panel.EnableDeleteOption(not FMD_NO_DELETE & style)
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=wx.ID_SAVE)

    def OnSave(self, evt):
        """Exit the dialog"""
        self.EndModal(wx.ID_OK)


class FileMgrPanel(wx.Panel):

    def __init__(self, parent, path, fname, filter):
        wx.Panel.__init__(self, parent)
        self._entry = wx.TextCtrl(self)
        self._flist = None
        self._path = path
        self._filter = filter
        self.__DoLayout(fname)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=wx.ID_DELETE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=wx.ID_SAVE)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=wx.ID_DELETE)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnFileSelected)
        return

    def __DoLayout(self, fname):
        """Layout the panel
        @param fname: default filename

        """
        vsizer = wx.BoxSizer(wx.VERTICAL)
        statbox = wx.StaticBox(self)
        sbsizer = wx.StaticBoxSizer(statbox, wx.VERTICAL)
        self._flist = FileList(self)
        self._flist.LoadFiles(self._path, self._filter)
        sbsizer.Add(self._flist, 1, wx.EXPAND)
        item = self._flist.FindItem(0, fname)
        if item != wx.NOT_FOUND:
            self._flist.Select(item)
        fbtnsz = wx.BoxSizer(wx.HORIZONTAL)
        dbtn = wx.Button(self, wx.ID_DELETE)
        if wx.Platform == '__WXMAC__':
            dbtn.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)
        fbtnsz.AddStretchSpacer()
        fbtnsz.Add(dbtn, 0, wx.ALIGN_RIGHT | wx.RIGHT, 5)
        sbsizer.Add((5, 5), 0)
        sbsizer.Add(fbtnsz, 0, wx.EXPAND)
        vsizer.Add((10, 10), 0)
        vsizer.Add(sbsizer, 1, wx.EXPAND | wx.ALL, 5)
        vsizer.Add((10, 10), 0)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sa_lbl = wx.StaticText(self, label=_('Save As'))
        hsizer.AddMany([(sa_lbl, 0, wx.ALIGN_CENTER_VERTICAL),
         ((5, 5), 0),
         (
          self._entry, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)])
        self._entry.SetValue(fname)
        vsizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 10)
        vsizer.Add((10, 10), 0)
        save = wx.Button(self, wx.ID_SAVE)
        cancel = wx.Button(self, wx.ID_CANCEL)
        cancel.SetDefault()
        bsizer = wx.StdDialogButtonSizer()
        bsizer.AddButton(save)
        bsizer.AddButton(cancel)
        bsizer.Realize()
        vsizer.Add(bsizer, 0, wx.EXPAND | wx.BOTTOM, 8)
        self.SetSizer(vsizer)

    def EnableDeleteOption(self, enable=True):
        """Enable/Disable the Delete Option
        @keyword enable: bool

        """
        del_btn = self.FindWindowById(wx.ID_DELETE)
        del_btn.Show(enable)
        self.Layout()

    @ecbasewin.expose(FileMgrDialog)
    def GetSelectedFile(self):
        """Get the selected filename
        @return: string

        """
        item = self._flist.GetFocusedItem()
        if item != -1:
            item = self._flist.GetItem(item, 0)
            fname = item.GetText()
            return fname
        return ''

    def OnDelete(self, evt):
        """Prompt to delete file the selected file"""
        fname = self.GetSelectedFile()
        if fname and os.path.exists(fname):
            if wx.MessageBox(_('Are you sure want to delete %s?') % fname, _('Delete File?'), wx.ICON_WARNING | wx.OK | wx.CANCEL | wx.CENTER, self) == wx.OK:
                try:
                    os.remove(fname)
                except OSError:
                    wx.MessageBox(_('Unable to delete %s') % fname, _('Delete Error'), wx.ICON_ERROR | wx.OK | wx.CENTER)
                else:
                    self._flist.DeleteAllItems()
                    self._flist.LoadFiles(self._path, self._filter)

    def OnFileSelected(self, evt):
        """Update the name in the save as field when a selection is made
        in the list control.

        """
        fname = self.GetSelectedFile()
        self._entry.SetValue(fname)

    def OnUpdateUI(self, evt):
        """Enable/Disable the Save button depending on what is entered in the
        filename dialog.

        """
        e_id = evt.GetId()
        if e_id == wx.ID_SAVE:
            evt.Enable(bool(self._entry.GetValue()))
        elif e_id == wx.ID_DELETE:
            evt.Enable(self._flist.GetFirstSelected() != -1)


class FileList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, elistmix.ListRowHighlighter):

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        elistmix.ListRowHighlighter.__init__(self)
        self.InsertColumn(0, _('Files'))
        il = wx.ImageList(16, 16)
        self.imgidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_MENU, (16,
                                                                                        16)))
        self.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        self.setResizeColumn(0)

    def LoadFiles(self, path, wildcards='*'):
        """Load all files from the given path
        @param path: directory to list
        @keyword wildcards: ; separated string of wildcard patterns

        """
        assert os.path.exists(path), 'Invalid Path'
        flist = list()
        patterns = wildcards.split(';')
        for fname in os.listdir(path):
            for pattern in patterns:
                if fnmatch.fnmatchcase(fname, pattern):
                    flist.append(fname)
                    break

        flist.sort()
        self.SetFiles(flist)

    def SetFiles(self, files):
        """Set the files in the list
        @param files: list of files

        """
        for (idx, fname) in enumerate(files):
            self.Append((fname,))
            self.SetItemImage(self.GetItemCount() - 1, self.imgidx)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    dlg = FileMgrDialog(frame, title='HELLO', defaultFile='eclutil.py', style=FMD_DEFAULT_STYLE)
    dlg.ShowModal()
    frame.Destroy()
    app.MainLoop()