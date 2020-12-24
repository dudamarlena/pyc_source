# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_panels/textdrop.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 4358 bytes
import wx, os
dirname = os.path.expanduser('~')
data_files = []
get = wx.GetApp()
USER_FILESAVE = get.USERfilesave

class TextDnD(wx.Panel):
    __doc__ = '\n    Accept one or more urls separated by a white space or newline.\n\n    '

    def __init__(self, parent):
        """
        """
        self.parent = parent
        self.file_dest = dirname if not USER_FILESAVE else USER_FILESAVE
        wx.Panel.__init__(self, parent=parent)
        self.textCtrl = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_MULTILINE | wx.TE_DONTWRAP))
        btn_clear = wx.Button(self, wx.ID_CLEAR, '')
        self.btn_save = wx.Button(self, (wx.ID_OPEN), '...', size=(-1, -1))
        self.text_path_save = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER | wx.TE_READONLY))
        self.lbl = wx.StaticText(self, label=(_('Add one or more URLs below')))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lbl, 0, wx.ALL, 5)
        sizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizer_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer_ctrl.Add(btn_clear, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_ctrl.Add(self.btn_save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_ctrl.Add(self.text_path_save, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.deleteAll, btn_clear)
        self.text_path_save.SetValue(self.file_dest)

    def topic_Redirect(self):
        """
        Redirects data to specific panel
        """
        if not self.textCtrl.GetValue():
            return
        data = self.textCtrl.GetValue().split()
        return data

    def deleteAll(self, event):
        """
        Delete and clear all text lines of the TxtCtrl

        """
        self.textCtrl.Clear()

    def on_file_save(self, path):
        """
        Set a specific directory for files saving

        """
        self.text_path_save.SetValue('')
        self.text_path_save.AppendText(path)
        self.file_dest = '%s' % path

    def statusbar_msg(self, mess, color):
        """
        Set a status bar message of the parent method.
        """
        self.parent.statusbar_msg('%s' % mess, color)