# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seb/git/kipartman/kipartman/frames/edit_part_storage_frame.py
# Compiled at: 2018-04-17 09:38:30
from dialogs.dialog_edit_part_storage import DialogEditPartStorage
from frames.select_storage_frame import SelectStorageFrame
from frames.dropdown_frame import DropdownFrame
import wx, rest

class EditPartStorageFrame(DialogEditPartStorage):

    def __init__(self, parent):
        super(EditPartStorageFrame, self).__init__(parent)

    def AddStorage(self, part):
        self.Title = 'Add storage'
        self.button_validate.Label = 'Add'
        self.part = part
        self.part_storage = rest.model.PartStorage(quantity=0)
        self.button_storage.Label = '<None>'
        self.storage = None
        self.spin_quantity.Value = 0
        result = self.ShowModal()
        if result == wx.ID_OK:
            return self.part_storage
        else:
            return

    def EditStorage(self, part, storage):
        self.Title = 'Edit storage'
        self.button_validate.Label = 'Apply'
        self.part = part
        self.part_storage = storage
        if storage:
            self.button_storage.Label = storage.name
        else:
            self.button_storage.Label = '<None>'
        self.storage = None
        self.spin_quantity.Value = self.part_storage.quantity
        result = self.ShowModal()
        if result == wx.ID_OK:
            return self.part_storage
        else:
            return

    def onButtonPartStorageClick(self, event):
        frame = DropdownFrame(self.button_storage, SelectStorageFrame, self.storage)
        frame.Dropdown(self.onSetStorageCallback)

    def onSetStorageCallback(self, storage):
        if storage:
            self.button_storage.Label = storage.name
        else:
            self.button_storage.Label = '<none>'
        self.storage = storage

    def onValidateClick(self, event):
        if self.button_storage.Label == '<None>':
            raise Exception('No storage selected')
        if self.storage:
            self.part_storage.id = self.storage.id
            self.part_storage.name = self.storage.name
            self.part_storage.description = self.storage.description
            self.part_storage.comment = self.storage.comment
        self.part_storage.quantity = self.spin_quantity.Value
        self.EndModal(wx.ID_OK)

    def onCancelClick(self, event):
        self.EndModal(wx.ID_CANCEL)