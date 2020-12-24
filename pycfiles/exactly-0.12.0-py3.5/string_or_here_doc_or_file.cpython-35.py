# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/documentation/string_or_here_doc_or_file.py
# Compiled at: 2020-01-15 22:55:33
# Size of source mod 2**32: 2703 bytes
from typing import List
from exactly_lib.common.help.syntax_contents_structure import SyntaxElementDescription
from exactly_lib.definitions import instruction_arguments
from exactly_lib.definitions.cross_ref.name_and_cross_ref import cross_reference_id_list
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.test_case_utils.documentation.relative_path_options_documentation import path_elements
from exactly_lib.test_case_utils.parse import parse_here_doc_or_path
from exactly_lib.test_case_utils.parse.rel_opts_configuration import RelOptionArgumentConfiguration
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.structure.core import ParagraphItem
from exactly_lib.util.textformat.textformat_parser import TextParser

class StringOrHereDocOrFile:

    def __init__(self, path_name: str, relativity_syntax_element_name: str, path_argument_configuration: RelOptionArgumentConfiguration, path_description_str: str):
        self._path_name = path_name
        self._relativity_syntax_element_name = relativity_syntax_element_name
        self._path_argument_configuration = path_argument_configuration
        self._expected_file_arg = a.Option(parse_here_doc_or_path.FILE_ARGUMENT_OPTION, path_name)
        self._path_description_str = path_description_str
        format_map = {'expected_file_arg': path_name}
        self._parser = TextParser(format_map)

    @property
    def path_name(self) -> str:
        return self._path_name

    @property
    def path_argument_configuration(self) -> RelOptionArgumentConfiguration:
        return self._path_argument_configuration

    def argument_usage(self, multiplicity: a.Multiplicity) -> a.ArgumentUsage:
        return a.Choice(multiplicity, [
         instruction_arguments.STRING,
         instruction_arguments.HERE_DOCUMENT,
         self._expected_file_arg])

    def syntax_element_descriptions(self) -> List[SyntaxElementDescription]:
        return path_elements(self._path_name, self._path_argument_configuration.options, self._paragraphs(self._path_description_str))

    def see_also_targets(self) -> list:
        return cross_reference_id_list([
         syntax_elements.PATH_SYNTAX_ELEMENT,
         syntax_elements.HERE_DOCUMENT_SYNTAX_ELEMENT,
         syntax_elements.STRING_SYNTAX_ELEMENT])

    def _paragraphs(self, s: str, extra: dict=None) -> List[ParagraphItem]:
        return self._parser.fnap(s, extra)