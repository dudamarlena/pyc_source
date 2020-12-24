# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/file_matcher.py
# Compiled at: 2020-01-29 09:40:37
# Size of source mod 2**32: 1033 bytes
import os
from abc import ABC, abstractmethod
from exactly_lib.symbol.logic.matcher import MatcherSdv
from exactly_lib.test_case_utils.file_properties import FileType
from exactly_lib.type_system.data.path_ddv import DescribedPath
from exactly_lib.type_system.logic.matcher_base_class import MatcherWTraceAndNegation, MatcherDdv, MatcherAdv

class FileTypeAccess(ABC):

    @abstractmethod
    def is_type(self, expected: FileType) -> bool:
        pass

    @abstractmethod
    def stat(self, follow_sym_links=True) -> os.stat_result:
        pass


class FileMatcherModel(ABC):

    @property
    @abstractmethod
    def path(self) -> DescribedPath:
        """Path of the file to match. May or may not exist."""
        pass

    @property
    @abstractmethod
    def file_type_access(self) -> FileTypeAccess:
        pass


FileMatcher = MatcherWTraceAndNegation[FileMatcherModel]
FileMatcherAdv = MatcherAdv[FileMatcherModel]
FileMatcherDdv = MatcherDdv[FileMatcherModel]
GenericFileMatcherSdv = MatcherSdv[FileMatcherModel]