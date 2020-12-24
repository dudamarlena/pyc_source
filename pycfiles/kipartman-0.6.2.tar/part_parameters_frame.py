# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/part_parameters_frame.py
# Compiled at: 2018-07-16 12:07:24
from dialogs.panel_part_parameters import PanelPartParameters
from frames.edit_part_parameter_frame import EditPartParameterFrame
import helper.tree

class DataModelPartParameter(helper.tree.TreeContainerItem):

    def __init__(self, part, parameter):
        super(DataModelPartParameter, self).__init__()
        self.part = part
        self.parameter = parameter

    def value_string(self, value, prefix, unit):
        res = ''
        if value is None:
            return res
        else:
            res = res + '%g' % value
            if prefix is not None:
                res = res + prefix.symbol
            if unit is not None:
                res = res + unit.symbol
            return res

    def min_string(self):
        return self.value_string(self.parameter.min_value, self.parameter.min_prefix, self.parameter.unit)

    def nom_string(self):
        return self.value_string(self.parameter.nom_value, self.parameter.nom_prefix, self.parameter.unit)

    def max_string(self):
        return self.value_string(self.parameter.max_value, self.parameter.max_prefix, self.parameter.unit)

    def unit_string(self):
        if self.parameter.unit is None:
            return ''
        else:
            return self.parameter.unit.name

    def GetValue(self, col):
        value_parameter = False
        if self.part.value_parameter and self.part.value_parameter == self.parameter.name:
            value_parameter = True
        if self.parameter.numeric == True:
            vMap = {0: value_parameter, 1: self.parameter.name, 
               2: self.min_string(), 
               3: self.nom_string(), 
               4: self.max_string(), 
               5: self.unit_string(), 
               6: self.parameter.description}
        else:
            vMap = {0: value_parameter, 1: self.parameter.name, 
               2: '', 
               3: self.parameter.text_value, 
               4: '', 
               5: self.unit_string(), 
               6: self.parameter.description}
        return vMap[col]

    def IsContainer(self):
        return False


class PartParametersFrame(PanelPartParameters):

    def __init__(self, parent):
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartParametersFrame, self).__init__(parent)
        self.enabled = False
        self.tree_parameters_manager = helper.tree.TreeManager(self.tree_parameters, context_menu=self.menu_parameter)
        self.tree_parameters_manager.AddToggleColumn('*')
        self.tree_parameters_manager.AddTextColumn('Parameter')
        self.tree_parameters_manager.AddTextColumn('Min Value')
        self.tree_parameters_manager.AddTextColumn('Nominal Value')
        self.tree_parameters_manager.AddTextColumn('Max Value')
        self.tree_parameters_manager.AddTextColumn('Unit')
        self.tree_parameters_manager.AddTextColumn('Description')
        self.tree_parameters_manager.OnItemBeforeContextMenu = self.onTreeParametersBeforeContextMenu
        self.tree_parameters_manager.OnItemValueChanged = self.onTreeParametersItemValueChanged
        self.cancel = None
        self.result = None
        self.enable(False)
        return

    def SetResult(self, result, cancel=None):
        """
        Callbacks for parent dialog
        """
        self.result = result
        self.cancel = cancel

    def SetPart(self, part):
        self.part = part
        self.showParameters()

    def enable(self, enabled=True):
        self.enabled = enabled

    def AddParameter(self, parameter):
        """
        Add a parameter to the part, or update if parameter already exists
        """
        if self.ExistParameter(parameter.name):
            self.RemoveParameter(parameter.name)
        if self.part.parameters is None:
            self.part.parameters = []
        self.part.parameters.append(parameter)
        self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))
        return

    def ExistParameter(self, name):
        """
        Test if a parameter exists by its name
        """
        if not self.part.parameters:
            return False
        for param in self.part.parameters:
            if param.name == name:
                return True

        return False

    def FindParameter(self, name):
        for data in self.tree_parameters_manager.data:
            if data.parameter.name == name:
                return data

        return

    def RemoveParameter(self, name):
        """
        Remove a parameter using its name
        """
        if not self.part.parameters:
            return False
        else:
            parameterobj = self.FindParameter(name)
            self.part.parameters.remove(parameterobj.parameter)
            self.tree_parameters_manager.DeleteItem(None, parameterobj)
            return

    def showParameters(self):
        self.tree_parameters_manager.ClearItems()
        if self.part and self.part.parameters:
            for parameter in self.part.parameters:
                self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))

        return

    def onTreeParametersBeforeContextMenu(self, event):
        item = self.tree_parameters.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_parameters_manager.ItemToObject(item)
        self.menu_parameter_add_parameter.Enable(True)
        self.menu_parameter_edit_parameter.Enable(True)
        self.menu_parameter_remove_parameter.Enable(True)
        if isinstance(obj, DataModelPartParameter) == False:
            self.menu_parameter_edit_parameter.Enable(False)
            self.menu_parameter_remove_parameter.Enable(False)
        if self.enabled == False:
            self.menu_parameter_add_parameter.Enable(False)
            self.menu_parameter_edit_parameter.Enable(False)
            self.menu_parameter_remove_parameter.Enable(False)
        return

    def onTreeParametersItemValueChanged(self, event):
        if self.enabled == False:
            return
        else:
            item = self.tree_parameters.GetSelection()
            if item.IsOk() == False:
                return
            parameterobj = self.tree_parameters_manager.ItemToObject(item)
            if self.part.value_parameter and parameterobj.parameter.name == self.part.value_parameter:
                self.part.value_parameter = None
            else:
                self.part.value_parameter = parameterobj.parameter.name
            return

    def onMenuParameterAddParameter(self, event):
        parameter = EditPartParameterFrame(self).AddParameter(self.part)
        if parameter is not None:
            self.part.parameters.append(parameter)
            self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))
        return

    def onMenuParameterEditParameter(self, event):
        item = self.tree_parameters.GetSelection()
        if item.IsOk() == False:
            return
        parameterobj = self.tree_parameters_manager.ItemToObject(item)
        parameter = EditPartParameterFrame(self).EditParameter(self.part, parameterobj.parameter)
        self.tree_parameters_manager.UpdateItem(parameterobj)

    def onMenuParameterRemoveParameter(self, event):
        item = self.tree_parameters.GetSelection()
        if item.IsOk() == False:
            return
        else:
            parameterobj = self.tree_parameters_manager.ItemToObject(item)
            self.part.parameters.remove(parameterobj.parameter)
            self.tree_parameters_manager.DeleteItem(None, parameterobj)
            return