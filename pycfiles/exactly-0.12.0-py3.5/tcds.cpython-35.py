# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_file_structure/tcds.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 595 bytes
from exactly_lib.test_case_file_structure.home_directory_structure import HomeDirectoryStructure
from exactly_lib.test_case_file_structure.sandbox_directory_structure import SandboxDirectoryStructure

class Tcds:
    __doc__ = 'Test Case Directory Structure'

    def __init__(self, hds: HomeDirectoryStructure, sds: SandboxDirectoryStructure):
        self._hds = hds
        self._sds = sds

    @property
    def hds(self) -> HomeDirectoryStructure:
        return self._hds

    @property
    def sds(self) -> SandboxDirectoryStructure:
        return self._sds