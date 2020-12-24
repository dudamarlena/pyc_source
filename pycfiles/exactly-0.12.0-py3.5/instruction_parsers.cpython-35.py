# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/element_parsers/instruction_parsers.py
# Compiled at: 2018-08-03 07:19:58
# Size of source mod 2**32: 1032 bytes
from exactly_lib.section_document import model
from exactly_lib.section_document.element_parsers.section_element_parsers import InstructionParser
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.source_location import FileSystemLocationInfo

class InstructionParserThatConsumesCurrentLine(InstructionParser):
    __doc__ = '\n    A parser that unconditionally consumes the current line,\n    and that uses the remaining part of the current line for\n    constructing the parsed instruction.\n\n    The parser cannot consume any more than the current line.\n\n    Precondition: The source must have a current line.\n    '

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> model.Instruction:
        rest_of_line = source.remaining_part_of_current_line
        source.consume_current_line()
        return self._parse(rest_of_line)

    def _parse(self, rest_of_line: str) -> model.Instruction:
        raise NotImplementedError()