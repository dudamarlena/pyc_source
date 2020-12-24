# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/manufacturers_frame.py
# Compiled at: 2018-04-29 13:46:26
from dialogs.panel_manufacturers import PanelManufacturers
import wx, rest, helper.tree
from helper.exception import print_stack

def NoneValue(value, default):
    if value:
        return value
    return default


class DataModelManufacturer(helper.tree.TreeItem):

    def __init__(self, manufacturer):
        super(DataModelManufacturer, self).__init__()
        self.manufacturer = manufacturer

    def GetValue(self, col):
        vMap = {0: self.manufacturer.name}
        return vMap[col]


class TreeManagerManufacturers(helper.tree.TreeManager):

    def __init__(self, tree_view):
        super(TreeManagerManufacturers, self).__init__(tree_view)

    def FindManufacturer(self, manufacturer_id):
        for data in self.data:
            if isinstance(data, DataModelManufacturer) and data.manufacturer.id == manufacturer_id:
                return data

        return

    def UpdateManufacturer(self, manufacturer):
        manufacturerobj = self.FindManufacturer(manufacturer.id)
        if manufacturerobj is None:
            return
        else:
            self.UpdateItem(manufacturerobj)
            return


class ManufacturersFrame(PanelManufacturers):

    def __init__(self, parent):
        super(ManufacturersFrame, self).__init__(parent)
        self.tree_manufacturers_manager = TreeManagerManufacturers(self.tree_manufacturers)
        self.tree_manufacturers_manager.AddTextColumn('name')
        self.tree_manufacturers_manager.OnSelectionChanged = self.onTreeManufacturersSelChanged
        self.panel_edit_manufacturer.Enabled = False
        self.panel_manufacturers.Enabled = True
        self.load()

    def loadManufacturers(self):
        self.tree_manufacturers_manager.ClearItems()
        manufacturers = rest.api.find_manufacturers()
        for manufacturer in manufacturers:
            self.tree_manufacturers_manager.AppendItem(None, DataModelManufacturer(manufacturer))

        return

    def load(self):
        try:
            self.loadManufacturers()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def ShowManufacturer(self, manufacturer):
        self.manufacturer = manufacturer
        if manufacturer:
            self.edit_manufacturer_name.Value = NoneValue(manufacturer.name, '')
            self.edit_manufacturer_address.Value = NoneValue(manufacturer.address, '')
            self.edit_manufacturer_website.Value = NoneValue(manufacturer.website, '')
            self.edit_manufacturer_email.Value = NoneValue(manufacturer.email, '')
            self.edit_manufacturer_phone.Value = NoneValue(manufacturer.phone, '')
            self.edit_manufacturer_comment.Value = NoneValue(manufacturer.comment, '')
        else:
            self.edit_manufacturer_name.Value = ''
            self.edit_manufacturer_address.Value = ''
            self.edit_manufacturer_website.Value = ''
            self.edit_manufacturer_email.Value = ''
            self.edit_manufacturer_phone.Value = ''
            self.edit_manufacturer_comment.Value = ''

    def onButtonAddManufacturerClick(self, event):
        self.ShowManufacturer(None)
        self.panel_edit_manufacturer.Enabled = True
        self.panel_manufacturers.Enabled = False
        return

    def onButtonEditManufacturerClick(self, event):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk() == False:
            return
        manufacturer = self.tree_manufacturers_manager.ItemToObject(item)
        self.ShowManufacturer(manufacturer.manufacturer)
        self.panel_edit_manufacturer.Enabled = True
        self.panel_manufacturers.Enabled = False

    def onButtonRemoveManufacturerClick(self, event):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk() == False:
            return
        else:
            manufacturer = self.tree_manufacturers_manager.ItemToObject(item)
            rest.api.delete_manufacturer(manufacturer.manufacturer.id)
            self.tree_manufacturers_manager.DeleteItem(None, manufacturer)
            return

    def onButtonRefreshManufacturersClick(self, event):
        self.load()

    def onTreeManufacturersSelChanged(self, event):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk() == False:
            return
        manufacturer = self.tree_manufacturers_manager.ItemToObject(item)
        self.ShowManufacturer(manufacturer.manufacturer)

    def onApplyButtonClick(self, event):
        if self.manufacturer is None:
            manufacturer = rest.model.ManufacturerNew()
        else:
            manufacturer = self.manufacturer
        manufacturer.name = self.edit_manufacturer_name.Value
        manufacturer.address = self.edit_manufacturer_address.Value
        manufacturer.website = self.edit_manufacturer_website.Value
        manufacturer.email = self.edit_manufacturer_email.Value
        manufacturer.phone = self.edit_manufacturer_phone.Value
        manufacturer.comment = self.edit_manufacturer_comment.Value
        try:
            if self.manufacturer is None:
                manufacturer = rest.api.add_manufacturer(manufacturer)
                self.tree_manufacturers_manager.AppendItem(None, DataModelManufacturer(manufacturer))
            else:
                manufacturer = rest.api.update_manufacturer(manufacturer.id, manufacturer)
                self.tree_manufacturers_manager.UpdateManufacturer(manufacturer)
            self.panel_edit_manufacturer.Enabled = False
            self.panel_manufacturers.Enabled = True
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        return

    def onCancelButtonClick(self, event):
        self.panel_edit_manufacturer.Enabled = False
        self.panel_manufacturers.Enabled = True