# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seb/git/kipartman/kipartman/frames/part_manufacturers_frame.py
# Compiled at: 2018-04-25 05:32:07
from dialogs.panel_part_manufacturers import PanelPartManufacturers
from frames.edit_part_manufacturer_frame import EditPartManufacturerFrame
import helper.tree

class DataModelPartManufacturer(helper.tree.TreeContainerItem):

    def __init__(self, manufacturer):
        super(DataModelPartManufacturer, self).__init__()
        self.manufacturer = manufacturer

    def GetValue(self, col):
        vMap = {0: self.manufacturer.name, 
           1: self.manufacturer.part_name}
        return vMap[col]

    def IsContainer(self):
        return False


class PartManufacturersFrame(PanelPartManufacturers):

    def __init__(self, parent):
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartManufacturersFrame, self).__init__(parent)
        self.tree_manufacturers_manager = helper.tree.TreeManager(self.tree_manufacturers)
        self.tree_manufacturers_manager.AddTextColumn('Manufacturer')
        self.tree_manufacturers_manager.AddTextColumn('Part Name')
        self.enable(False)

    def SetPart(self, part):
        self.part = part
        self.showManufacturers()

    def enable(self, enabled=True):
        self.button_add_manufacturer.Enabled = enabled
        self.button_edit_manufacturer.Enabled = enabled
        self.button_remove_manufacturer.Enabled = enabled

    def FindManufacturer(self, name):
        for data in self.tree_manufacturers_manager.data:
            if data.manufacturer.name == name:
                return data

        return

    def AddManufacturer(self, manufacturer):
        """
        Add a manufacturer to the part
        """
        if self.part.manufacturers is None:
            self.part.manufacturers = []
        self.part.manufacturers.append(manufacturer)
        self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))
        return

    def RemoveManufacturer(self, name):
        """
        Remove a manufacturer using its name
        """
        if self.part.manufacturers is None or len(self.part.manufacturers) == 0:
            return
        manufacturerobj = self.FindManufacturer(name)
        self.part.manufacturers.remove(manufacturerobj)
        self.tree_manufacturers_manager.DeleteItem(None, manufacturerobj)
        return

    def showManufacturers(self):
        self.tree_manufacturers_manager.ClearItems()
        if self.part and self.part.manufacturers:
            for manufacturer in self.part.manufacturers:
                self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))

        return

    def onButtonAddManufacturerClick(self, event):
        manufacturer = EditPartManufacturerFrame(self).AddManufacturer(self.part)
        if manufacturer:
            if self.part.manufacturers is None:
                self.part.manufacturers = []
            self.part.manufacturers.append(manufacturer)
            self.tree_manufacturers_manager.AppendItem(None, DataModelPartManufacturer(manufacturer))
        return

    def onButtonEditManufacturerClick(self, event):
        item = self.tree_manufacturers.GetSelection()
        if not item.IsOk():
            return
        manufacturerobj = self.tree_manufacturers_manager.ItemToObject(item)
        EditPartManufacturerFrame(self).EditManufacturer(self.part, manufacturerobj.manufacturer)
        self.tree_manufacturers_manager.UpdateItem(manufacturerobj)

    def onButtonRemoveManufacturerClick(self, event):
        item = self.tree_manufacturers.GetSelection()
        if not item:
            return
        else:
            manufacturerobj = self.tree_manufacturers_manager.ItemToObject(item)
            self.part.manufacturers.remove(manufacturerobj.manufacturer)
            self.tree_manufacturers_manager.DeleteItem(None, manufacturerobj)
            return