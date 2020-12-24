# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_file_structure/home_directory_structure.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 799 bytes
import pathlib
from exactly_lib.test_case_file_structure.path_relativity import RelHdsOptionType

class HomeDirectoryStructure(tuple):

    def __new__(cls, case_dir: pathlib.Path, act_dir: pathlib.Path):
        return tuple.__new__(cls, (case_dir,
         act_dir,
         {RelHdsOptionType.REL_HDS_CASE: case_dir, 
          RelHdsOptionType.REL_HDS_ACT: act_dir}))

    @property
    def case_dir(self) -> pathlib.Path:
        return self[0]

    @property
    def act_dir(self) -> pathlib.Path:
        return self[1]

    def get(self, d: RelHdsOptionType) -> pathlib.Path:
        return self[2][d]