# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/edit_wish_frame.py
# Compiled at: 2017-10-01 05:26:02
from dialogs.dialog_edit_wish import DialogEditWish
import wx

class EditWishFrame(DialogEditWish):

    def __init__(self, parent):
        super(EditWishFrame, self).__init__(parent)

    def addWish(self, type):
        self.Title = 'Add wish'
        self.button_validate.LabelText = 'Add'
        result = self.ShowModal()
        if result == wx.ID_OK:
            wish = type(quantity=self.spin_quantity.GetValue())
            return wish
        else:
            return

    def editWish(self, wish):
        self.Title = 'Edit wish'
        self.button_validate.LabelText = 'Apply'
        self.spin_quantity.SetValue(wish.quantity)
        result = self.ShowModal()
        if result == wx.ID_OK:
            wish.quantity = self.spin_quantity.GetValue()
            return wish
        else:
            return

    def onValidateClick(self, event):
        self.EndModal(wx.ID_OK)

    def onCancelClick(self, event):
        self.EndModal(wx.ID_CANCEL)