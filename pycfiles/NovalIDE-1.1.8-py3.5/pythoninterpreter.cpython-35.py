# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/project/pages/pythoninterpreter.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 2447 bytes
from noval import _
import tkinter as tk
from tkinter import ttk
import noval.python.interpreter.interpretermanager as interpretermanager, noval.util.utils as utils, noval.consts as consts, noval.python.project.runconfiguration as runconfiguration, noval.project.property as projectproperty, noval.ui_utils as ui_utils, noval.ttkwidgets.linklabel as linklabel, noval.ui_common as ui_common

class PythonInterpreterPanel(ui_utils.BaseConfigurationPanel):

    def __init__(self, parent, item, current_project):
        ui_utils.BaseConfigurationPanel.__init__(self, parent)
        self._current_project = current_project
        row = ttk.Frame(self)
        interpreterLabelText = ttk.Label(row, text=_('Interpreter:')).pack(fill='x', side=tk.LEFT)
        choices, default_selection = interpretermanager.InterpreterManager().GetChoices()
        self.interpreterCombo = ttk.Combobox(row, values=choices)
        self.interpreterCombo['state'] = 'readonly'
        self.interpreterCombo.pack(fill='x', side=tk.LEFT, expand=1)
        row.pack(fill='x')
        if len(choices) > 0:
            self.interpreterCombo.current(default_selection)
        hyperLinkCtrl = linklabel.LinkLabel(self, text=_('Click to configure interpreters not listed'), normal_color='royal blue', hover_color='blue', clicked_color='purple')
        hyperLinkCtrl.bind('<Button-1>', self.GotoInterpreterConfiguration)
        hyperLinkCtrl.pack(fill='x', pady=consts.DEFAUT_HALF_CONTRL_PAD_Y)
        project_interpreter_name = runconfiguration.ProjectConfiguration.LoadProjectInterpreter(current_project.GetKey())
        if project_interpreter_name and project_interpreter_name in choices:
            self.interpreterCombo.current(choices.index(project_interpreter_name))

    def OnOK(self, optionsDialog):
        utils.profile_set(self._current_project.GetKey() + '/Interpreter', self.GetInterpreter().Name)
        return True

    def GotoInterpreterConfiguration(self, event):
        if not ui_common.ShowInterpreterConfigurationPage():
            return
        choices, default_selection = interpretermanager.InterpreterManager().GetChoices()
        self.interpreterCombo['values'] = choices
        if len(choices) > 0:
            self.interpreterCombo.current(default_selection)

    def GetInterpreter(self):
        return interpretermanager.InterpreterManager().interpreters[self.interpreterCombo.current()]