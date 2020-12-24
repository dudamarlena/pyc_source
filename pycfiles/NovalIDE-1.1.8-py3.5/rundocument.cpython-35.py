# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/project/rundocument.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 14284 bytes
from noval import _
from noval.project.document import ProjectDocument
from noval.python.debugger.executor import *
from noval.python.debugger.commandproperty import *
import noval.python.project.model as pyprojectlib, noval.python.pyutils as pyutils, uuid
from noval.python.debugger.commandui import *
import noval.python.project.runconfiguration as runconfiguration, noval.consts as consts

class PythonProjectDocument(ProjectDocument):

    def __init__(self, model=None):
        ProjectDocument.__init__(self, model)

    @staticmethod
    def GetProjectModel():
        return pyprojectlib.PythonProject()

    def GetFileRunConfiguration(self, run_file):
        """
            获取单个文件的运行配置,单个文件有多个运行配置,每个运行配置的运行方式是不同的
        """
        file_key = self.GetFileKey(run_file)
        run_configuration_name = utils.profile_get(file_key + '/RunConfigurationName', '')
        return run_configuration_name

    def GetRunfileParameter(self, run_file):
        """
            获取项目要运行单个python文件的运行参数
        """
        run_configuration_name = self.GetFileRunConfiguration(run_file)
        if run_configuration_name:
            file_configuration = runconfiguration.FileConfiguration(self, run_file)
            run_configuration = file_configuration.LoadConfiguration(run_configuration_name)
            try:
                return run_configuration.GetRunParameter()
            except PromptErrorException as e:
                wx.MessageBox(e.msg, _('Error'), wx.OK | wx.ICON_ERROR)
                return

            use_argument = utils.profile_get_int(self.GetFileKey(run_file, 'UseArgument'), True)
            if use_argument:
                initialArgs = utils.profile_get(self.GetFileKey(run_file, 'RunArguments'), '')
        else:
            initialArgs = ''
        python_path = utils.profile_get(self.GetFileKey(run_file, 'PythonPath'), '')
        startIn = utils.profile_get(self.GetFileKey(run_file, 'RunStartIn'), '')
        if startIn == '':
            startIn = os.path.dirname(self.GetFilename())
        env = {}
        paths = set()
        path_post_end = utils.profile_get_int(self.GetKey('PythonPathPostpend'), True)
        if path_post_end:
            paths.add(str(os.path.dirname(self.GetFilename())))
        if len(python_path) > 0:
            paths.add(str(python_path))
        env[consts.PYTHON_PATH_NAME] = os.pathsep.join(list(paths))
        return self.GetRunconfigClass()(GetApp().GetCurrentInterpreter(), run_file.filePath, initialArgs, env, startIn, project=self)

    def SaveRunParameter(self, run_parameter):
        project_name = os.path.basename(self.GetFilename())
        utils.profile_set(self.GetKey('LastRunProject'), project_name)
        utils.profile_set(self.GetKey('LastRunFile'), run_parameter.FilePath)
        utils.profile_set(self.GetKey('LastRunArguments'), run_parameter.Arg)
        utils.profile_set(self.GetKey('LastRunStartIn'), run_parameter.StartupPath)
        if run_parameter.Environment is not None and consts.PYTHON_PATH_NAME in run_parameter.Environment:
            utils.profile_set(self.GetKey('LastPythonPath'), run_parameter.Environment[consts.PYTHON_PATH_NAME])

    def DebugRunBuiltin(self, run_parameter):
        fileToRun = run_parameter.FilePath
        GetApp().MainFrame.ShowView(consts.PYTHON_INTERPRETER_VIEW_NAME, toogle_visibility_flag=True)
        python_interpreter_view = GetApp().MainFrame.GetCommonView(consts.PYTHON_INTERPRETER_VIEW_NAME)
        old_argv = sys.argv
        environment, initialArgs = run_parameter.Environment, run_parameter.Arg
        sys.argv = [fileToRun]
        command = 'execfile(r"%s")' % fileToRun
        python_interpreter_view.run(command)
        sys.argv = old_argv

    def GetRunConfiguration(self, run_file=None):
        """
            获取项目的当前运行配置,也就是默认启动文件的运行配置
        """
        if run_file is None:
            run_configuration_key = self.GetKey()
        else:
            run_configuration_key = self.GetFileKey(run_file)
        run_configuration_name = utils.profile_get(run_configuration_key + '/RunConfigurationName', '')
        return run_configuration_name

    def GetFileRunParameter(self, filetoRun=None, is_break_debug=False):
        if self.GetModel().Id == ProjectDocument.UNPROJECT_MODEL_ID or filetoRun is not None and self.GetModel().FindFile(filetoRun) is None:
            doc_view = self.GetDebugger().GetActiveView()
            if doc_view:
                document = doc_view.GetDocument()
                if not document.Save() or document.IsNewDocument:
                    return
                if self.GetDebugger().IsFileContainBreakPoints(document) or is_break_debug:
                    messagebox.showwarning(GetApp().GetAppName(), _('Debugger can only run in active project'))
            else:
                return
            run_parameter = document.GetRunParameter()
        else:
            if filetoRun is None:
                run_file = self.GetandSetProjectStartupfile()
            else:
                run_file = self.GetModel().FindFile(filetoRun)
            if not run_file:
                return
            self.PromptToSaveFiles()
            run_parameter = self.GetRunfileParameter(run_file)
        return run_parameter

    def IsProjectContainBreakPoints(self):
        masterBPDict = GetApp().MainFrame.GetView(consts.BREAKPOINTS_TAB_NAME).GetMasterBreakpointDict()
        for key in masterBPDict:
            if self.GetModel().FindFile(key) and len(masterBPDict[key]) > 0:
                return True

        return False

    def GetRunParameter(self, filetoRun=None, is_break_debug=False):
        """
            @is_break_debug:user force to debug breakpoint or not
        """
        if not PythonExecutor.GetPythonExecutablePath():
            return
        is_debug_breakpoint = False
        run_configuration_name = self.GetRunConfiguration()
        if filetoRun is None and run_configuration_name:
            project_configuration = runconfiguration.ProjectConfiguration(self)
            run_configuration = project_configuration.LoadConfiguration(run_configuration_name)
            if not run_configuration:
                run_parameter = self.GetFileRunParameter(filetoRun, is_break_debug)
            else:
                run_parameter = run_configuration.GetRunParameter()
        else:
            run_parameter = self.GetFileRunParameter(filetoRun, is_break_debug)
        if run_parameter is None:
            return
        if self.IsProjectContainBreakPoints():
            is_debug_breakpoint = True
        run_parameter = pyutils.get_override_runparameter(run_parameter)
        run_parameter.IsBreakPointDebug = is_debug_breakpoint
        return run_parameter

    def Debug(self):
        run_parameter = self.GetRunParameter()
        if run_parameter is None:
            return
        if not run_parameter.IsBreakPointDebug:
            self.DebugRunScript(run_parameter)
        else:
            self.DebugrunBreakpoint(run_parameter)
        self.GetDebugger().AppendRunParameter(run_parameter)

    def DebugRunScript(self, run_parameter):
        if run_parameter.Interpreter.IsBuiltIn:
            self.DebugRunBuiltin(run_parameter)
            return
        fileToRun = run_parameter.FilePath
        shortFile = os.path.basename(fileToRun)
        view = GetApp().MainFrame.AddView('Debugger' + str(uuid.uuid1()).lower(), RunCommandUI, _('Running: ') + shortFile, 's', visible_by_default=True, image_file='python/debugger/debug.ico', debugger=self.GetDebugger(), run_parameter=run_parameter, visible_in_menu=False)
        page = view['instance']
        page.Execute()
        GetApp().GetDocumentManager().ActivateView(self.GetDebugger().GetView())

    def RunWithoutDebug(self, filetoRun=None):
        run_parameter = self.GetRunParameter(filetoRun)
        if run_parameter is None:
            return
        run_parameter.IsBreakPointDebug = False
        self.DebugRunScript(run_parameter)
        self.GetDebugger().AppendRunParameter(run_parameter)

    def Run(self, filetoRun=None):
        run_parameter = self.GetRunParameter(filetoRun)
        if run_parameter is None:
            return
        self.RunScript(run_parameter)
        self.GetDebugger().AppendRunParameter(run_parameter)

    def RunScript(self, run_parameter):
        interpreter = run_parameter.Interpreter
        if interpreter.IsBuiltIn:
            return
        executor = PythonrunExecutor(run_parameter)
        executor.Execute()

    def GetLastRunParameter(self, is_debug):
        if not PythonExecutor.GetPythonExecutablePath():
            return
        dlg_title = _('Run File')
        btn_name = _('Run')
        if is_debug:
            dlg_title = _('Debug File')
            btn_name = _('Debug')
        dlg = CommandPropertiesDialog(GetApp().GetTopWindow(), dlg_title, self, okButtonName=btn_name, debugging=is_debug, is_last_config=True)
        showDialog = dlg.MustShowDialog()
        is_parameter_save = False
        if showDialog and dlg.ShowModal() == constants.ID_OK:
            projectDocument, fileToDebug, initialArgs, startIn, isPython, environment = dlg.GetSettings()
            is_parameter_save = True
        else:
            if not showDialog:
                dlg.withdraw()
                projectDocument, fileToDebug, initialArgs, startIn, isPython, environment = dlg.GetSettings()
                dlg.destroy()
            else:
                dlg.destroy()
                return
            if self.GetFilename() != consts.NOT_IN_ANY_PROJECT and self.IsProjectContainBreakPoints():
                is_debug_breakpoint = True
            else:
                is_debug_breakpoint = False
        run_parameter = runconfig.PythonRunconfig(GetApp().GetCurrentInterpreter(), fileToDebug, initialArgs, environment, startIn, is_debug_breakpoint)
        if is_parameter_save:
            self.SaveRunParameter(run_parameter)
        return run_parameter

    def DebugRunLast(self):
        run_parameter = self.GetLastRunParameter(True)
        if run_parameter is None:
            return
        run_parameter = pyutils.get_override_runparameter(run_parameter)
        if not run_parameter.IsBreakPointDebug:
            self.DebugRunScript(run_parameter)
        else:
            self.DebugRunScriptBreakPoint(run_parameter)

    def RunLast(self):
        run_parameter = self.GetLastRunParameter(False)
        if run_parameter is None:
            return
        run_parameter = pyutils.get_override_runparameter(run_parameter)
        self.RunScript(run_parameter)

    def SetParameterAndEnvironment(self):
        dlg = CommandPropertiesDialog(GetApp().GetTopWindow(), _('Set Parameter And Environment'), self, okButtonName=_('&OK'))
        dlg.ShowModal()

    def BreakintoDebugger(self, filetoRun=None):
        run_parameter = self.GetRunParameter(filetoRun, is_break_debug=True)
        if run_parameter is None or run_parameter.Project is None:
            return
        run_parameter.IsBreakPointDebug = True
        self.DebugrunBreakpoint(run_parameter, autoContinue=False)

    def DebugrunBreakpoint(self, run_parameter, autoContinue=True):
        """
            autoContinue可以让断点调式是否会在开始中断
        """
        if BaseDebuggerUI.DebuggerRunning():
            messagebox.showinfo(_('Debugger Running'), _('A debugger is already running. Please shut down the other debugger first.'))
            return
        host = utils.profile_get('DebuggerHostName', DEFAULT_HOST)
        if not host:
            wx.MessageBox(_('No debugger host set. Please go to Tools->Options->Debugger and set one.'), _('No Debugger Host'))
            return
        fileToRun = run_parameter.FilePath
        shortFile = os.path.basename(fileToRun)
        view = GetApp().MainFrame.AddView('Debugger' + str(uuid.uuid1()).lower(), PythonDebuggerUI, _('Debugging: ') + shortFile, 's', visible_by_default=True, image_file='python/debugger/debugger.png', debugger=self.GetDebugger(), run_parameter=run_parameter, visible_in_menu=False, autoContinue=autoContinue)
        page = view['instance']
        page.Execute()
        self.GetDebugger().SetDebuggerUI(page)
        GetApp().GetDocumentManager().ActivateView(self.GetDebugger().GetView())