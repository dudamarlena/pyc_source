# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/select_part_frame.py
# Compiled at: 2018-07-16 12:07:24
from dialogs.panel_select_part import PanelSelectPart
import wx, wx.lib.newevent, wx.dataview, rest
from frames.parts_frame import DataModelCategory, DataModelCategoryPath, DataModelPart, TreeManagerParts
from part_parameters_frame import DataModelPartParameter
import helper.tree
SelectPartOkEvent, EVT_SELECT_PART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectPartCancelEvent, EVT_SELECT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()

class SelectPartFrame(PanelSelectPart):

    def __init__(self, parent, initial=None):
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectPartFrame, self).__init__(parent)
        self.tree_parts_manager = TreeManagerParts(self.tree_parts)
        self.tree_parts_manager.AddIntegerColumn('id')
        self.tree_parts_manager.AddTextColumn('name')
        self.tree_parts_manager.AddTextColumn('description')
        self.tree_parts_manager.AddIntegerColumn('comment')
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelectionChanged
        self.tree_parameters_manager = helper.tree.TreeManager(self.tree_parameters)
        self.tree_parameters_manager.AddToggleColumn('*')
        self.tree_parameters_manager.AddTextColumn('Parameter')
        self.tree_parameters_manager.AddTextColumn('Min Value')
        self.tree_parameters_manager.AddTextColumn('Nominal Value')
        self.tree_parameters_manager.AddTextColumn('Max Value')
        self.tree_parameters_manager.AddTextColumn('Unit')
        self.tree_parameters_manager.AddTextColumn('Description')
        self.search_filter = None
        self.search_part.Value = ''
        self.load()
        self.cancel = None
        self.result = None
        return

    def load(self):
        self.tree_parts_manager.ClearItems()
        if self.search_filter:
            parts = rest.api.find_parts(search=self.search_filter)
        else:
            parts = rest.api.find_parts()
        categories = {}
        for part in parts:
            if part.category:
                category_name = part.category.path
            else:
                category_name = '/'
            if categories.has_key(category_name) == False:
                categories[category_name] = DataModelCategoryPath(part.category)
                self.tree_parts_manager.AppendItem(None, categories[category_name])
            self.tree_parts_manager.AppendItem(categories[category_name], DataModelPart(part, {}))

        for category in categories:
            self.tree_parts_manager.Expand(categories[category])

        return

    def showParameters(self, part):
        self.tree_parameters_manager.ClearItems()
        if part and part.parameters:
            for parameter in part.parameters:
                self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(part, parameter))

        return

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel

    def onTreePartsSelectionChanged(self, event):
        item = self.tree_parts.GetSelection()
        if item.IsOk() == False:
            return
        partobj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(partobj, DataModelPart) == False:
            return
        partobj.part = rest.api.find_part(partobj.part.id, with_parameters=True)
        self.showParameters(partobj.part)

    def onButtonCancelClick(self, event):
        event = SelectPartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()

    def onButtonOkClick(self, event):
        item = self.tree_parts.GetSelection()
        if item.IsOk() == False:
            return
        partobj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(partobj, DataModelPart) == False:
            return
        event = SelectPartOkEvent(data=partobj.part)
        wx.PostEvent(self, event)
        if self.result:
            self.result(partobj.part)

    def onSearchPartCancelButton(self, event):
        self.search_filter = None
        self.load()
        return

    def onSearchPartSearchButton(self, event):
        self.search_filter = self.search_part.Value
        self.load()

    def onSearchPartTextEnter(self, event):
        self.search_filter = self.search_part.Value
        self.load()