# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/cli/program_modes/symbol/impl/report.py
# Compiled at: 2019-12-27 10:07:29
# Size of source mod 2**32: 645 bytes
from abc import ABC, abstractmethod
from typing import Sequence
from exactly_lib.cli.program_modes.symbol.impl.reports.symbol_info import DefinitionsResolver
from exactly_lib.util.simple_textstruct.structure import MajorBlock

class ReportBlock(ABC):

    @abstractmethod
    def render(self) -> MajorBlock:
        pass


class Report(ABC):

    @property
    @abstractmethod
    def is_success(self) -> bool:
        pass

    @abstractmethod
    def blocks(self) -> Sequence[ReportBlock]:
        pass


class ReportGenerator(ABC):

    @abstractmethod
    def generate(self, definitions_resolver: DefinitionsResolver) -> Report:
        pass