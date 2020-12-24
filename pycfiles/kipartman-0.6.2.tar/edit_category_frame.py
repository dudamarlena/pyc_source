# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/edit_category_frame.py
# Compiled at: 2017-08-10 04:30:16
from dialogs.dialog_edit_category import DialogEditCategory
import wx

class EditCategoryFrame(DialogEditCategory):

    def __init__(self, parent):
        super(EditCategoryFrame, self).__init__(parent)

    def addCategory(self, type):
        self.Title = 'Add category'
        self.button_validate.LabelText = 'Add'
        result = self.ShowModal()
        if result == wx.ID_OK:
            category = type(name=self.text_name.Value, description=self.text_description.Value)
            return category
        else:
            return

    def editCategory(self, category):
        self.Title = 'Edit category'
        self.button_validate.LabelText = 'Apply'
        self.text_name.Value = category.name
        self.text_description.Value = category.description
        result = self.ShowModal()
        if result == wx.ID_OK:
            category.name = self.text_name.Value
            category.description = self.text_description.Value
            return category
        else:
            return

    def onValidateClick(self, event):
        self.EndModal(wx.ID_OK)

    def onCancelClick(self, event):
        self.EndModal(wx.ID_CANCEL)