# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/section_parsing.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1864 bytes
from typing import Sequence, Dict
from exactly_lib.section_document.section_element_parsing import SectionElementParser

class SectionConfiguration(tuple):

    def __new__(cls, section_name: str, parser: SectionElementParser):
        return tuple.__new__(cls, (section_name, parser))

    @property
    def section_name(self) -> str:
        return self[0]

    @property
    def parser(self) -> SectionElementParser:
        return self[1]


class SectionsConfiguration:
    __doc__ = '\n    Sections and their instruction parser.\n    '

    def __init__(self, parsers_for_named_sections: Sequence[SectionConfiguration], default_section_name: str=None,
                 section_element_name_for_error_messages: str='section'):
        self.section_element_name_for_error_messages = section_element_name_for_error_messages
        self._parsers_for_named_sections = parsers_for_named_sections
        self._section2parser = {pfs.section_name:pfs.parser for pfs in parsers_for_named_sections}
        self.default_section_name = default_section_name
        if default_section_name is not None and default_section_name not in self._section2parser:
            raise ValueError('The name of the default section "%s" does not correspond to any section: %s' % (
             default_section_name,
             str(self._section2parser.keys())))

    def sections(self) -> Dict[(str, SectionElementParser)]:
        return self._section2parser

    def parser_for_section(self, section_name: str) -> SectionElementParser:
        return self._section2parser[section_name]

    def has_section(self, section_name: str) -> bool:
        return section_name in self._section2parser