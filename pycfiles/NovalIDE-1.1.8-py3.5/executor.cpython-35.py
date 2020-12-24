# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/debugger/executor.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 4452 bytes
from noval import GetApp, _
from tkinter import messagebox
import noval.project.executor as executor, noval.util.strutils as strutils, noval.ui_common as ui_common, noval.util.utils as utils, tempfile, subprocess

class CommonExecutorMixin:

    def __init__(self):
        self.is_windows_application = self._run_parameter.IsWindowsApplication()
        if self.is_windows_application:
            self._path = self._run_parameter.Interpreter.WindowPath
        else:
            self._path = self._run_parameter.Interpreter.Path
        self._cmd = strutils.emphasis_path(self._path)
        if self._run_parameter.InterpreterOption and self._run_parameter.InterpreterOption != ' ':
            self._cmd = self._cmd + ' ' + self._run_parameter.InterpreterOption


class PythonExecutor(executor.Executor, CommonExecutorMixin):

    def GetPythonExecutablePath():
        current_interpreter = GetApp().GetCurrentInterpreter()
        if current_interpreter:
            return current_interpreter.Path
        messagebox.showinfo(_('Python Executable Location Unknown'), _("To proceed we need to know the location of the python.exe you would like to use.\nTo set this, go to Tools-->Options and use the 'Python Inpterpreter' panel to configuration a interpreter.\n"))
        ui_common.ShowInterpreterConfigurationPage()

    GetPythonExecutablePath = staticmethod(GetPythonExecutablePath)

    def __init__(self, run_parameter, wxComponent, callbackOnExit=None, source=executor.SOURCE_DEBUG, cmd_contain_path=True):
        executor.Executor.__init__(self, run_parameter, wxComponent, callbackOnExit, source)
        assert self._run_parameter.Interpreter != None
        CommonExecutorMixin.__init__(self)
        if cmd_contain_path:
            self._cmd += self.spaceAndQuote(self._run_parameter.FilePath)
        self._stdOutReader = None
        self._stdErrReader = None
        self._process = None


class PythonrunExecutor(executor.TerminalExecutor, CommonExecutorMixin):

    def __init__(self, run_parameter):
        executor.TerminalExecutor.__init__(self, run_parameter)
        CommonExecutorMixin.__init__(self)
        self._cmd += self.spaceAndQuote(self._run_parameter.FilePath)

    def Execute(self):
        command = self.GetExecuteCommand()
        if self.is_windows_application:
            utils.get_logger().debug('start run executable: %s', command)
            temp_file = tempfile.TemporaryFile()
            subprocess.Popen(command, shell=False, cwd=self.GetStartupPath(), env=self._run_parameter.Environment, stdout=temp_file.fileno(), stderr=temp_file.fileno())
        else:
            executor.TerminalExecutor.Execute(self)


class PythonDebuggerExecutor(PythonExecutor):

    def __init__(self, debugger_fileName, run_parameter, wxComponent, arg1=None, arg2=None, arg3=None, arg4=None, arg5=None, arg6=None, arg7=None, arg8=None, arg9=None, callbackOnExit=None):
        super(PythonDebuggerExecutor, self).__init__(run_parameter, wxComponent, callbackOnExit, cmd_contain_path=False)
        self._debugger_fileName = debugger_fileName
        self._cmd += self.spaceAndQuote(self._debugger_fileName)
        if arg1 != None:
            self._cmd += self.spaceAndQuote(arg1)
        if arg2 != None:
            self._cmd += self.spaceAndQuote(arg2)
        if arg3 != None:
            self._cmd += self.spaceAndQuote(arg3)
        if arg4 != None:
            self._cmd += self.spaceAndQuote(arg4)
        if arg5 != None:
            self._cmd += self.spaceAndQuote(arg5)
        if arg6 != None:
            self._cmd += self.spaceAndQuote(arg6)
        if arg7 != None:
            self._cmd += self.spaceAndQuote(arg7)
        if arg8 != None:
            self._cmd += self.spaceAndQuote(arg8)
        if arg9 != None:
            self._cmd += self.spaceAndQuote(arg9)