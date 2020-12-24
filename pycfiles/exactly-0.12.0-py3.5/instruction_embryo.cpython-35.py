# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/multi_phase/utils/instruction_embryo.py
# Compiled at: 2020-02-02 12:38:29
# Size of source mod 2**32: 3119 bytes
from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Generic
from exactly_lib.section_document.element_parsers import token_stream_parser
from exactly_lib.section_document.element_parsers.token_stream_parser import TokenParser
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.source_location import FileSystemLocationInfo
from exactly_lib.symbol.symbol_usage import SymbolUsage
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, PhaseLoggingPaths
from exactly_lib.test_case.validation.sdv_validation import SdvValidator, ConstantSuccessSdvValidator
T = TypeVar('T')

class MainStepExecutorEmbryo(Generic[T], ABC):
    __doc__ = '\n    Executor with standard arguments, but custom return type.\n    \n    The custom return type makes testing easier, by providing access to\n    custom result.\n    '

    @abstractmethod
    def main(self, environment: InstructionEnvironmentForPostSdsStep, logging_paths: PhaseLoggingPaths, os_services: OsServices) -> T:
        pass


class InstructionEmbryo(Generic[T], MainStepExecutorEmbryo[T], ABC):
    __doc__ = '\n    Instruction embryo that makes it easy to both\n    test using custom information (in sub classes),\n    and integrate into many phases.\n    \n    A multi-phase instruction may sub class this class,\n    to achieve both easy testing (by giving access to things that\n    are specific for the instruction in question),\n    and integrate into different phases.\n    '

    @property
    def symbol_usages(self) -> Sequence[SymbolUsage]:
        return []

    @property
    def validator(self) -> SdvValidator:
        return ConstantSuccessSdvValidator()


class InstructionEmbryoParser(Generic[T]):

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> InstructionEmbryo[T]:
        raise NotImplementedError()


class InstructionEmbryoParserWoFileSystemLocationInfo(Generic[T], InstructionEmbryoParser[T]):

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> InstructionEmbryo[T]:
        return self._parse(source)

    def _parse(self, source: ParseSource) -> InstructionEmbryo[T]:
        raise NotImplementedError('abstract method')


class InstructionEmbryoParserFromTokensWoFileSystemLocationInfo(Generic[T], InstructionEmbryoParser[T], ABC):

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> InstructionEmbryo[T]:
        return self._parse(source)

    def _parse(self, source: ParseSource) -> InstructionEmbryo[T]:
        with token_stream_parser.from_parse_source(source, consume_last_line_if_is_at_eol_after_parse=True) as (token_parser):
            return self._parse_from_tokens(token_parser)

    @abstractmethod
    def _parse_from_tokens(self, token_parser: TokenParser) -> InstructionEmbryo[T]:
        pass