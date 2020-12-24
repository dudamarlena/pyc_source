# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/concrete_path_parts.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 918 bytes
from exactly_lib.type_system.data.path_part import PathPartDdv

class PathPartDdvAsFixedPath(PathPartDdv):

    def __init__(self, file_name: str):
        self._file_name = file_name

    def value(self) -> str:
        return self._file_name


class PathPartDdvAsNothing(PathPartDdv):

    def value(self) -> str:
        return ''


class PathPartDdvVisitor:

    def visit(self, path_suffix: PathPartDdv):
        if isinstance(path_suffix, PathPartDdvAsFixedPath):
            return self.visit_fixed_path(path_suffix)
        if isinstance(path_suffix, PathPartDdvAsNothing):
            return self.visit_nothing(path_suffix)
        raise TypeError('Not a {}: {}'.format(str(PathPartDdv), path_suffix))

    def visit_fixed_path(self, path_suffix: PathPartDdvAsFixedPath):
        raise NotImplementedError()

    def visit_nothing(self, path_suffix: PathPartDdvAsNothing):
        raise NotImplementedError()