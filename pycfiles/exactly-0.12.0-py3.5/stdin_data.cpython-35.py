# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/program/stdin_data.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1135 bytes
from typing import Sequence
from exactly_lib.test_case_file_structure.dir_dependent_value import DirDependentValue
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.data.string_or_path_ddvs import StringOrPathDdv, StringOrPath

class StdinData(tuple):
    __doc__ = '\n    Text that should become the stdin contents of a process.\n\n    Made up of zero or more fragments that should be concatenated.\n    '

    def __new__(cls, fragments: Sequence[StringOrPath]):
        return tuple.__new__(cls, (fragments,))

    @property
    def fragments(self) -> Sequence[StringOrPath]:
        return self[0]

    @property
    def is_empty(self) -> bool:
        return len(self.fragments) == 0


class StdinDataDdv(DirDependentValue[StdinData]):

    def __init__(self, fragments: Sequence[StringOrPathDdv]):
        self._fragments = fragments

    @property
    def fragments(self) -> Sequence[StringOrPathDdv]:
        return self._fragments

    def value_of_any_dependency(self, tcds: Tcds) -> StdinData:
        return StdinData([f.value_of_any_dependency(tcds) for f in self._fragments])