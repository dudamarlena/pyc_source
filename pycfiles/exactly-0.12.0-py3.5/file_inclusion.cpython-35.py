# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/directives/objects/file_inclusion.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 2645 bytes
from typing import Sequence
from exactly_lib.common.help.abs_or_rel_path import abs_or_rel_path_of_existing
from exactly_lib.common.help.syntax_contents_structure import InvokationVariant, invokation_variant_from_args, SyntaxElementDescription, cli_argument_syntax_element_description
from exactly_lib.definitions.entity import directives
from exactly_lib.help.entities.directives.contents_structure import DirectiveDocumentation
from exactly_lib.processing.parse import file_inclusion_directive_parser
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.structure.document import SectionContents
from exactly_lib.util.textformat.textformat_parser import TextParser

class FileInclusionDocumentation(DirectiveDocumentation):

    def __init__(self):
        super().__init__(directives.INCLUDING_DIRECTIVE_INFO)
        self.file_argument = a.Named(file_inclusion_directive_parser.FILE_ARGUMENT_NAME)
        self._tp = TextParser({'including_directive': self.info.singular_name, 
         'FILE': self.file_argument.name})

    def invokation_variants(self) -> Sequence[InvokationVariant]:
        return [
         invokation_variant_from_args([
          a.Single(a.Multiplicity.MANDATORY, self.file_argument)])]

    def syntax_element_descriptions(self) -> Sequence[SyntaxElementDescription]:
        return [
         cli_argument_syntax_element_description(self.file_argument, abs_or_rel_path_of_existing('file', self.file_argument.name, _FILE_RELATIVITY_ROOT))]

    def description(self) -> SectionContents:
        return docs.section_contents(self._tp.fnap(_MAIN_DESCRIPTION_REST))


_FILE_RELATIVITY_ROOT = 'directory of the current source file'
_MAIN_DESCRIPTION_REST = 'The effect of including a file is equivalent to having the\ncontents of the included file in the including file;\nexcept that the current phase of the including file\ncannot be changed by an included file.\n\n\nThe default phase of the included file is the phase\nfrom which the file is included.\n\n\nThe included file may contain contents of\ndifferent phases,\nby declaring different phases just as in a main test case file.\n\nBut the phase of the including file is\nnot changed.\n'