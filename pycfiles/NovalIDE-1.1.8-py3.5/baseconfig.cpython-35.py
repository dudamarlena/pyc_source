# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/project/baseconfig.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1461 bytes
import os

class NewProjectConfiguration:
    PROJECT_ADD_SRC_PATH = 1
    DEFAULT_PROJECT_SRC_PATH = 'Src'

    def __init__(self, name, location, is_project_dir_created):
        self._name = name
        self._location = location
        self._is_project_dir_created = is_project_dir_created

    @property
    def Name(self):
        return self._name

    @property
    def Location(self):
        return self._location

    @property
    def ProjectDirCreated(self):
        return self._is_project_dir_created


class BaseRunconfig:

    def __init__(self, exe_path, arg='', env=None, start_up=None, project=None):
        self._exe = exe_path
        self._arg = arg
        self._env = env
        self._start_up_path = start_up
        self._project = project

    @property
    def ExePath(self):
        return self._exe

    @property
    def Arg(self):
        return self._arg

    @property
    def Environment(self):
        return self._env

    @property
    def StartupPath(self):
        if not self._start_up_path:
            if self._project is None:
                return os.path.dirname(self.ExePath)
            return self._project.GetPath()
        return self._start_up_path

    @property
    def Project(self):
        return self._project