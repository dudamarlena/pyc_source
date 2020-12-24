# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/edit_storage_frame.py
# Compiled at: 2017-10-01 05:26:02
from dialogs.dialog_edit_storage import DialogEditStorage
import wx

class EditStorageFrame(DialogEditStorage):

    def __init__(self, parent):
        super(EditStorageFrame, self).__init__(parent)

    def addStorage(self, type):
        self.Title = 'Add storage'
        self.button_validate.LabelText = 'Add'
        result = self.ShowModal()
        if result == wx.ID_OK:
            storage = type(name=self.text_name.Value, description=self.text_description.Value, comment=self.text_comment.Value)
            return storage
        else:
            return

    def editStorage(self, storage):
        self.Title = 'Edit storage'
        self.button_validate.LabelText = 'Apply'
        self.text_name.Value = storage.name
        self.text_description.Value = storage.description
        self.text_comment.Value = storage.comment
        result = self.ShowModal()
        if result == wx.ID_OK:
            storage.name = self.text_name.Value
            storage.description = self.text_description.Value
            storage.comment = self.text_comment.Value
            return storage
        else:
            return

    def onValidateClick(self, event):
        self.EndModal(wx.ID_OK)

    def onCancelClick(self, event):
        self.EndModal(wx.ID_CANCEL)