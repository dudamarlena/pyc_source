# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/impl/path/value_str_renderers.py
# Compiled at: 2019-12-27 10:07:53
# Size of source mod 2**32: 1920 bytes
import pathlib
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.data import path_description
from exactly_lib.type_system.data.path_ddv import PathDdv
from exactly_lib.util.render.renderer import Renderer

class PathValueRelTcdsDir(Renderer[str]):

    def __init__(self, path_ddv: PathDdv):
        self._path_ddv = path_ddv

    def render(self) -> str:
        return path_description.path_ddv_with_relativity_name_prefix__rel_tcds_dir(self._path_ddv)


class PathValueRelCwd(Renderer[str]):

    def __init__(self, path_ddv: PathDdv, cwd: pathlib.Path, tcds: Tcds):
        self._path_ddv = path_ddv
        self._cwd = cwd
        self._tcds = tcds

    def render(self) -> str:
        return path_description.path_ddv_with_relativity_name_prefix(self._path_ddv, self._tcds, self._cwd)


class PathValueRelUnknownCwd(Renderer[str]):

    def __init__(self, path_ddv: PathDdv):
        self._path_ddv = path_ddv

    def render(self) -> str:
        return str(_CURRENT_DIRECTORY / self._path_ddv.path_suffix_path())


class PathValueAbsolute(Renderer[str]):

    def __init__(self, path_ddv: PathDdv, tcds: Tcds):
        self._path_ddv = path_ddv
        self._tcds = tcds

    def render(self) -> str:
        return path_description.path_ddv_with_relativity_name_prefix(self._path_ddv, self._tcds, None)


class PathValuePlainAbsolute(Renderer[str]):

    def __init__(self, path_ddv: PathDdv):
        self._path_ddv = path_ddv

    def render(self) -> str:
        return str(self._path_ddv.value_when_no_dir_dependencies())


_CURRENT_DIRECTORY = pathlib.Path('<CURRENT-DIRECTORY>')