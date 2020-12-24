# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/section_element_parsing.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 3548 bytes
from typing import Optional
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.parsed_section_element import ParsedSectionElement
from exactly_lib.section_document.source_location import FileSystemLocationInfo
from exactly_lib.util import line_source
from exactly_lib.util.line_source import line_sequence_from_line

class SectionElementError(Exception):
    __doc__ = '\n    An exceptions related to a line in the test case that is\n    expected to be parsed as a :class:SectionElement\n\n    Does not need to be aware of current file and section,\n    since this is taken care of by the document parsing framework.\n\n    I.e., this exception is used within the parsing of a document,\n    as communication between the parsing framework and element parsers.\n\n    This kind of exceptions is never thrown from a document parser.\n    '

    def __init__(self, source: line_source.LineSequence, message: str):
        self._source = source
        self._message = message

    @property
    def source(self) -> line_source.LineSequence:
        return self._source

    @property
    def message(self) -> str:
        return self._message


class UnrecognizedSectionElementSourceError(SectionElementError):
    __doc__ = '\n    The source is not recognized by the parser,\n    but may be recognized by another parser.\n\n    The parser must not have consumed any source.\n    '


class RecognizedSectionElementSourceError(SectionElementError):
    __doc__ = '\n    The source is recognized, in the meaning that the element\n    should be parsed by the parser raising this exception.\n\n    But the element source contains an unrecoverable error,\n    e.g. a syntax error in the arguments to a recognized instruction.\n\n    The parser may have consumed source.\n    '


def new_unrecognized_section_element_error_of_single_line(line: line_source.Line, message: str) -> SectionElementError:
    return UnrecognizedSectionElementSourceError(line_sequence_from_line(line), message)


def new_recognized_section_element_error_of_single_line(line: line_source.Line, message: str) -> SectionElementError:
    return RecognizedSectionElementSourceError(line_sequence_from_line(line), message)


class SectionElementParser:

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> Optional[ParsedSectionElement]:
        """
        Parser of a section element, represented by a :class:ParsedSectionElement

        The possibility to return None exists to help constructing parsers from parts -
        a return value of None means that some other parser may try to parse the same source,
        while a raised SourceError means that this parser recognizes the source (e.g. by
        being the name of an instruction), but that there is some syntax error related to
        the recognized element (e.g. instruction).

        :param fs_location_info: Information about the location of the source file being parsed
        :param source: Remaining source to parse

        :returns: None iff source is invalid / unrecognized. If None is returned, source must _not_
        have been consumed.
        :raises SectionElementError: The element cannot be parsed.
        """
        raise NotImplementedError('abstract method')