# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_panels/filedrop.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 10831 bytes
import wx, os
from videomass3.vdms_io import IO_tools
from videomass3.vdms_utils.utils import time_seconds
AZURE = '#d9ffff'
RED = '#ea312d'
YELLOW = '#a29500'
GREENOLIVE = '#6aaf23'
ORANGE = '#f28924'
dirname = os.path.expanduser('~')
data_files = []
get = wx.GetApp()
USER_FILESAVE = get.USERfilesave

class MyListCtrl(wx.ListCtrl):
    __doc__ = '\n    This is the listControl widget. Note that this wideget has DnDPanel\n    parent.\n    '

    def __init__(self, parent):
        """Constructor"""
        self.index = 0
        self.parent = parent
        wx.ListCtrl.__init__(self, parent, style=(wx.LC_REPORT | wx.LC_SINGLE_SEL))

    def dropUpdate(self, path):
        """
        Update list-control during drag and drop

        """
        msg_dir = _('Directories are not allowed, just add files, please.')
        if os.path.isdir(path):
            self.parent.statusbar_msg(msg_dir, ORANGE)
            return
        data = [x for x in data_files if x['format']['filename'] == path] or IO_tools.probeInfo(path)
        if data[1]:
            self.parent.statusbar_msg(data[1], RED)
            return
            data = eval(data[0])
            self.InsertItem(self.index, path)
            self.index += 1
            if 'duration' not in data['format'].keys():
                data['format']['duration'] = 0
            else:
                data.get('format')['time'] = data.get('format').pop('duration')
                t = time_seconds(data.get('format')['time'])
                data['format']['duration'] = t
            data_files.append(data)
            self.parent.statusbar_msg('', None)
        else:
            mess = _("Duplicate files are rejected: > '%s'") % path
            self.parent.statusbar_msg(mess, YELLOW)


class FileDrop(wx.FileDropTarget):
    __doc__ = '\n    This is the file drop target\n    '

    def __init__(self, window):
        """
        Constructor. File Drop targets are subsets of windows
        """
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, write where they were dropped and then
        the file paths themselves
        """
        for filepath in filenames:
            self.window.dropUpdate(filepath)

        return True


class FileDnD(wx.Panel):
    __doc__ = '\n    Panel for dragNdrop files queue. Accept one or more files.\n    '

    def __init__(self, parent):
        """Constructor. This will initiate with an id and a title"""
        self.parent = parent
        self.file_dest = dirname if not USER_FILESAVE else USER_FILESAVE
        self.selected = None
        wx.Panel.__init__(self, parent=parent)
        self.flCtrl = MyListCtrl(self)
        file_drop_target = FileDrop(self.flCtrl)
        self.flCtrl.SetDropTarget(file_drop_target)
        btn_clear = wx.Button(self, wx.ID_CLEAR, '')
        self.btn_save = wx.Button(self, (wx.ID_OPEN), '...', size=(-1, -1))
        self.text_path_save = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER | wx.TE_READONLY))
        self.lbl = wx.StaticText(self, label=(_('Drag one or more files below')))
        self.flCtrl.InsertColumn(0, '', width=700)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lbl, 0, wx.ALL, 5)
        sizer.Add(self.flCtrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizer_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer_ctrl.Add(btn_clear, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_ctrl.Add(self.btn_save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_ctrl.Add(self.text_path_save, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.deleteAll, btn_clear)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.flCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect, self.flCtrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_doubleClick, self.flCtrl)
        self.Bind(wx.EVT_CONTEXT_MENU, self.onContext)
        self.text_path_save.SetValue(self.file_dest)

    def on_Redirect(self):
        """
        Redirects data to specific panel
        """
        if self.flCtrl.GetItemCount() == 0:
            return
        return data_files

    def which(self):
        """
        return topic name by choose_topic.py selection

        """
        return self.parent.topicname

    def onContext(self, event):
        """
        Create and show a Context Menu
        """
        if not hasattr(self, 'popupID1'):
            self.popupID1 = wx.NewId()
            self.Bind((wx.EVT_MENU), (self.onPopup), id=(self.popupID1))
        menu = wx.Menu()
        itemThree = menu.Append(self.popupID1, _('Remove the selected file'))
        self.PopupMenu(menu)
        menu.Destroy()

    def onPopup(self, event):
        """
        Evaluate the label string of the menu item selected and starts
        the related process
        """
        itemId = event.GetId()
        menu = event.GetEventObject()
        menuItem = menu.FindItemById(itemId)
        if not self.selected:
            self.parent.statusbar_msg(_('No file selected to `%s` yet') % menuItem.GetLabel(), 'GOLDENROD')
        else:
            self.parent.statusbar_msg('Add Files', None)
            if menuItem.GetLabel() == _('Remove the selected file'):
                if self.flCtrl.GetItemCount() == 1:
                    self.deleteAll(self)
                else:
                    item = self.flCtrl.GetFocusedItem()
                    self.flCtrl.DeleteItem(item)
                    self.selected = None
                    data_files.pop(item)

    def deleteAll(self, event):
        """
        Delete and clear all text lines of the TxtCtrl,
        reset the fileList[], disable Toolbar button and menu bar
        Stream/play select imported file - Stream/display imported...
        """
        self.flCtrl.DeleteAllItems()
        del data_files[:]
        self.parent.filedropselected = None
        self.selected = None

    def on_select(self, event):
        """
        Selecting a line with mouse or up/down keyboard buttons
        """
        index = self.flCtrl.GetFocusedItem()
        item = self.flCtrl.GetItemText(index)
        self.parent.filedropselected = item
        self.selected = item

    def on_doubleClick(self, row):
        """
        Double click or keyboard enter button, open media info
        """
        self.onContext(self)

    def on_deselect(self, event):
        """
        De-selecting a line with mouse by click in empty space of
        the control list
        """
        self.parent.filedropselected = None
        self.selected = None

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