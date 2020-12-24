# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/processing/parse/file_inclusion_directive_parser.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 2113 bytes
import pathlib
from typing import Optional
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.parsed_section_element import ParsedFileInclusionDirective
from exactly_lib.section_document.section_element_parsing import SectionElementParser, RecognizedSectionElementSourceError
from exactly_lib.section_document.source_location import FileSystemLocationInfo
from exactly_lib.util.line_source import line_sequence_from_line
FILE_ARGUMENT_NAME = 'FILE'

class FileInclusionDirectiveParser(SectionElementParser):
    __doc__ = '\n    Element parser that parses a :class:`ParsedFileInclusionDirective`\n\n    Syntax:\n\n      DIRECTIVE_NAME PATH\n\n    PATH uses Posix syntax\n\n    DIRECTIVE_NAME is a string given to the constructor, that must not contain space.\n\n\n    The parser returns None iff the source is not a line that starts with DIRECTIVE_NAME\n    '

    def __init__(self, directive_token: str):
        """
        :param directive_token: The directive token that precedes the path. Must not contain space.
        """
        self._directive_token = directive_token

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> Optional[ParsedFileInclusionDirective]:
        parts = source.current_line_text.strip().split()
        if len(parts) == 0 or parts[0] != self._directive_token:
            return
        directive_source = line_sequence_from_line(source.current_line)
        source.consume_current_line()
        if len(parts) == 1:
            raise RecognizedSectionElementSourceError(directive_source, 'Missing {} argument'.format(FILE_ARGUMENT_NAME))
        if len(parts) != 2:
            raise RecognizedSectionElementSourceError(directive_source, 'Superfluous arguments: ' + ' '.join(parts[2:]))
        path = pathlib.Path(pathlib.PurePosixPath(parts[1]))
        return ParsedFileInclusionDirective(directive_source, [
         path])