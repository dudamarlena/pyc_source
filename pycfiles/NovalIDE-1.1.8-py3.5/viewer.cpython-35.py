# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/project/viewer.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 11574 bytes
from noval import _, GetApp
from tkinter import messagebox
from noval.project.baseviewer import *
import tkinter as tk
from tkinter import ttk
import noval.consts as consts, noval.ttkwidgets.linklabel as linklabel, noval.python.interpreter.interpretermanager as interpretermanager
from noval.python.project.runconfig import PythonNewProjectConfiguration, PythonRunconfig
import os, noval.python.parser.utils as dirutils, noval.project.command as command
from noval.project.templatemanager import ProjectTemplateManager
import noval.iface as iface, noval.plugin as plugin, noval.ui_common as ui_common, noval.ui_utils as ui_utils, noval.project.variables as variablesutils
from noval.project.document import ProjectDocument

class PythonProjectTemplate(ProjectTemplate):

    def CreateDocument(self, path, flags):
        return ProjectTemplate.CreateDocument(self, path, flags, wizard_cls=NewPythonProjectWizard)


class NewPythonProjectWizard(NewProjectWizard):

    def LoadDefaultProjectTemplates(self):
        """
            这里不能加载默认模板了,已经通过默认插件加载了对应的模板
        """
        pass


class BasePythonProjectNameLocationPage(ProjectNameLocationPage):

    def __init__(self, master, project_dir_option=True, **kwargs):
        ProjectNameLocationPage.__init__(self, master, project_dir_option=project_dir_option, **kwargs)

    def CreateNamePage(self, content_frame):
        name_frame = ProjectNameLocationPage.CreateNamePage(self, content_frame)
        self.interpreter_label = ttk.Label(name_frame, text=_('Interpreter:'))
        self.interpreter_label.grid(column=0, row=2, sticky='nsew')
        self.interpreter_entry_var = tk.StringVar()
        self.interpreter_combo = ttk.Combobox(name_frame, textvariable=self.interpreter_entry_var)
        names = interpretermanager.InterpreterManager().GetInterpreterNames()
        self.interpreter_combo.grid(column=1, row=2, sticky='nsew', padx=(consts.DEFAUT_HALF_CONTRL_PAD_X, 0), pady=(consts.DEFAUT_CONTRL_PAD_Y, 0))
        self.interpreter_combo.state(['readonly'])
        self.interpreter_combo['values'] = names
        if len(names) > 0:
            self.interpreter_combo.current(0)
        link_label = linklabel.LinkLabel(name_frame, text=_('Configuration'), normal_color='royal blue', hover_color='blue', clicked_color='purple')
        link_label.bind('<Button-1>', self.OpenInterpreterConfiguration)
        link_label.grid(column=2, row=2, sticky='nsew', padx=(consts.DEFAUT_HALF_CONTRL_PAD_X, 0), pady=(consts.DEFAUT_CONTRL_PAD_Y, 0))

    def OpenInterpreterConfiguration(self, *args):
        ui_common.ShowInterpreterConfigurationPage()

    def GetNewPojectConfiguration(self):
        return PythonNewProjectConfiguration(self.name_var.get(), self.dir_entry_var.get(), self.interpreter_entry_var.get(), self.project_dir_chkvar.get(), -1)


class PythonProjectNameLocationPage(BasePythonProjectNameLocationPage):

    def __init__(self, master, **kwargs):
        BasePythonProjectNameLocationPage.__init__(self, master, project_dir_option=False, **kwargs)

    def CreateContent(self, content_frame, **kwargs):
        BasePythonProjectNameLocationPage.CreateContent(self, content_frame, **kwargs)
        sizer_frame = ttk.Frame(content_frame)
        sizer_frame.grid(column=0, row=4, sticky='nsew')
        pythonpath_val = kwargs.get('pythonpath_pattern', PythonNewProjectConfiguration.PROJECT_SRC_PATH_ADD_TO_PYTHONPATH)
        self.pythonpath_chkvar = tk.IntVar(value=pythonpath_val)
        self.add_src_radiobutton = ttk.Radiobutton(sizer_frame, text=_('Create %s Folder And Add it to the PYTHONPATH') % PythonNewProjectConfiguration.DEFAULT_PROJECT_SRC_PATH, variable=self.pythonpath_chkvar, value=PythonNewProjectConfiguration.PROJECT_SRC_PATH_ADD_TO_PYTHONPATH)
        self.add_src_radiobutton.pack(fill='x', pady=(consts.DEFAUT_CONTRL_PAD_Y, 0))
        self.add_project_path_radiobutton = ttk.Radiobutton(sizer_frame, text=_('Add Project Directory to the PYTHONPATH'), variable=self.pythonpath_chkvar, value=PythonNewProjectConfiguration.PROJECT_PATH_ADD_TO_PYTHONPATH)
        self.add_project_path_radiobutton.pack(fill='x')
        self.configure_no_path_radiobutton = ttk.Radiobutton(sizer_frame, text=_("Don't Configure PYTHONPATH(later manually configure it)"), variable=self.pythonpath_chkvar, value=PythonNewProjectConfiguration.NONE_PATH_ADD_TO_PYTHONPATH)
        self.configure_no_path_radiobutton.pack(fill='x')
        ProjectNameLocationPage.CreateProjectDirPage(self, content_frame, chk_box_row=5, **kwargs)

    def Finish(self):
        if not ProjectNameLocationPage.Finish(self):
            return False
        dirName = self.GetProjectLocation()
        if self.pythonpath_chkvar.get() == PythonNewProjectConfiguration.PROJECT_SRC_PATH_ADD_TO_PYTHONPATH:
            project_src_path = os.path.join(dirName, PythonNewProjectConfiguration.DEFAULT_PROJECT_SRC_PATH)
            if not os.path.exists(project_src_path):
                try:
                    dirutils.MakeDirs(project_src_path)
                except Exception as e:
                    self.infotext_label_var.set('%s' % str(e))
                    return False

                view = GetApp().MainFrame.GetProjectView().GetView()
                doc = view.GetDocument()
                if self._new_project_configuration.PythonpathMode == PythonNewProjectConfiguration.PROJECT_PATH_ADD_TO_PYTHONPATH:
                    utils.profile_set(doc.GetKey() + '/AppendProjectPath', True)
        else:
            utils.profile_set(doc.GetKey() + '/AppendProjectPath', False)
        if self._new_project_configuration.PythonpathMode == PythonNewProjectConfiguration.PROJECT_SRC_PATH_ADD_TO_PYTHONPATH:
            doc.GetCommandProcessor().Submit(command.ProjectAddFolderCommand(view, doc, PythonNewProjectConfiguration.DEFAULT_PROJECT_SRC_PATH))
            src_path = os.path.join(variablesutils.FormatVariableName(variablesutils.PROJECT_DIR_VARIABLE), PythonNewProjectConfiguration.DEFAULT_PROJECT_SRC_PATH)
            utils.profile_set(doc.GetKey() + '/InternalPath', [src_path])
        return True

    def GetNewPojectConfiguration(self):
        return PythonNewProjectConfiguration(self.name_var.get(), self.dir_entry_var.get(), self.interpreter_entry_var.get(), self.project_dir_chkvar.get(), self.pythonpath_chkvar.get())


class PythonProjectView(ProjectView):
    PACKAGE_INIT_FILE = '__init__.py'

    def __init__(self, frame):
        ProjectView.__init__(self, frame)

    def AddFolderItem(self, document, folderPath):
        destfolderPath = os.path.join(document.GetModel().homeDir, folderPath)
        packageFilePath = os.path.join(destfolderPath, self.PACKAGE_INIT_FILE)
        is_package = False
        if os.path.exists(packageFilePath):
            is_package = True
        if not is_package:
            return ProjectView.AddFolderItem(self, document, folderPath)
        return self._treeCtrl.AddPackageFolder(folderPath)

    def OnAddPackageFolder(self):
        if self.GetDocument():
            items = self._treeCtrl.selection()
            if items:
                item = items[0]
                if self._IsItemFile(item):
                    item = self._treeCtrl.parent(item)
                folderDir = self._GetItemFolderPath(item)
            else:
                folderDir = ''
            if folderDir:
                folderDir += '/'
            folderPath = '%sPackage' % folderDir
            i = 1
            while self._treeCtrl.FindFolder(folderPath):
                i += 1
                folderPath = '%sPackage%s' % (folderDir, i)

            projectdir = self.GetDocument().GetModel().homeDir
            destpackagePath = os.path.join(projectdir, folderPath)
            try:
                os.mkdir(destpackagePath)
            except Exception as e:
                messagebox.showerror(GetApp().GetAppName(), str(e), parent=self.GetFrame())
                return

            self.GetDocument().GetCommandProcessor().Submit(command.ProjectAddPackagefolderCommand(self, self.GetDocument(), folderPath))
            destpackageFile = os.path.join(destpackagePath, self.PACKAGE_INIT_FILE)
            with open(destpackageFile, 'w') as (f):
                self.GetDocument().GetCommandProcessor().Submit(command.ProjectAddFilesCommand(self.GetDocument(), [destpackageFile], folderPath))
            item = self._treeCtrl.FindFolder(folderPath)
            self._treeCtrl.selection_set(item)
            self._treeCtrl.focus(item)
            self._treeCtrl.see(item)
            self.OnRename()

    def Run(self):
        selected_file_path = self.GetSelectedFilePath()
        GetApp().GetDebugger().Runfile(filetoRun=selected_file_path)

    def DebugRun(self):
        selected_file_path = self.GetSelectedFilePath()
        GetApp().GetDebugger().RunWithoutDebug(filetoRun=selected_file_path)

    def BreakintoDebugger(self):
        selected_file_path = self.GetSelectedFilePath()
        GetApp().GetDebugger().GetCurrentProject().BreakintoDebugger(filetoRun=selected_file_path)

    def GetSelectedFilePath(self):
        selected_file_path = self.GetSelectedFile()
        if selected_file_path is None and not fileutils.is_python_file(selected_file_path):
            return
        return selected_file_path

    def AddPackageFolder(self, folderPath):
        self._treeCtrl.AddPackageFolder(folderPath)
        return True

    def UpdateUI(self, command_id):
        if command_id in [constants.ID_ADD_PACKAGE_FOLDER]:
            return self.GetDocument() is not None
        else:
            return ProjectView.UpdateUI(self, command_id)


class DefaultProjectTemplateLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        ProjectTemplateManager().AddProjectTemplate('General', 'Empty Project', [PythonProjectNameLocationPage])
        ProjectTemplateManager().AddProjectTemplate('General', 'New Project From Existing Code', [
         (
          'noval.python.project.viewer.PythonProjectNameLocationPage',
          {'can_finish': False, 
           'pythonpath_pattern': PythonNewProjectConfiguration.PROJECT_PATH_ADD_TO_PYTHONPATH, 'create_project_dir': False}), ('noval.project.importfiles.ImportfilesPage', {'rejects': ProjectDocument.BIN_FILE_EXTS})])