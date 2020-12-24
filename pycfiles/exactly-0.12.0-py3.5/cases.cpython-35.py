# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/instruction_set/sections/cases.py
# Compiled at: 2019-11-19 10:15:33
# Size of source mod 2**32: 1361 bytes
from pathlib import Path
from typing import List
from exactly_lib.section_document.element_parsers.section_element_parsers import InstructionWithoutDescriptionParser, standard_syntax_element_parser, InstructionParserWithoutSourceFileLocationInfo
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.section_element_parsing import SectionElementParser
from exactly_lib.test_suite.instruction_set import utils
from exactly_lib.test_suite.instruction_set.instruction import Environment, TestSuiteFileReferencesInstruction

def new_parser() -> SectionElementParser:
    return standard_syntax_element_parser(InstructionWithoutDescriptionParser(_CasesSectionParser()))


class CasesSectionInstruction(TestSuiteFileReferencesInstruction):

    def __init__(self, resolver: utils.FileNamesResolver):
        self._resolver = resolver

    def resolve_paths(self, environment: Environment) -> List[Path]:
        return self._resolver.resolve(environment)


class _CasesSectionParser(InstructionParserWithoutSourceFileLocationInfo):

    def parse_from_source(self, source: ParseSource) -> CasesSectionInstruction:
        resolver = utils.parse_file_names_resolver(source, utils.single_regular_file_resolver)
        return CasesSectionInstruction(resolver)