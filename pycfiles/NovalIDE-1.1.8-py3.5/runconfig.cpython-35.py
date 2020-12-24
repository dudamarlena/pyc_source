# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/project/runconfig.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 2575 bytes
from noval.project.baseconfig import *
import noval.util.utils as utils

class PythonNewProjectConfiguration(NewProjectConfiguration):
    PROJECT_SRC_PATH_ADD_TO_PYTHONPATH = NewProjectConfiguration.PROJECT_ADD_SRC_PATH
    PROJECT_PATH_ADD_TO_PYTHONPATH = 2
    NONE_PATH_ADD_TO_PYTHONPATH = 3

    def __init__(self, name, location, interpreter, is_project_dir_created, pythonpath_mode):
        NewProjectConfiguration.__init__(self, name, location, is_project_dir_created)
        self._interpreter = interpreter
        self._pythonpath_mode = pythonpath_mode

    @property
    def Interpreter(self):
        return self._interpreter

    @property
    def PythonpathMode(self):
        return self._pythonpath_mode


class PythonRunconfig(BaseRunconfig):

    def __init__(self, interpreter, file_path, arg='', env=None, start_up=None, is_debug_breakpoint=False, project=None, interpreter_option=''):
        BaseRunconfig.__init__(self, interpreter.Path, interpreter_option, env, start_up, project)
        self._interpreter = interpreter
        self._file_path = file_path
        self._is_debug_breakpoint = is_debug_breakpoint
        self._interpreter_option = interpreter_option
        self._file_arg = arg

    @property
    def FilePath(self):
        return self._file_path

    @property
    def Interpreter(self):
        return self._interpreter

    @property
    def IsBreakPointDebug(self):
        return self._is_debug_breakpoint

    @IsBreakPointDebug.setter
    def IsBreakPointDebug(self, is_debug_breakpoint):
        self._is_debug_breakpoint = is_debug_breakpoint

    @property
    def InterpreterOption(self):
        return self._arg

    @property
    def Arg(self):
        return self._file_arg

    def IsWindowsApplication(self):
        """
            是否是windows应用程序,如果是则使用pythonw.exe解释器来运行程序,否则默认使用python.exe
        """
        if not self.Project:
            return False
        return utils.profile_get_int(self.Project.GetKey('IsWindowsApplication'), False) and utils.is_windows()

    @property
    def StartupPath(self):
        if not self._start_up_path:
            if self._project is None:
                return os.path.dirname(self.FilePath)
            return self._project.GetPath()
        return self._start_up_path