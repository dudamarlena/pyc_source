# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/types/objects/data_types.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 2648 bytes
from exactly_lib.common.help.documentation_text import POSIX_SYNTAX
from exactly_lib.definitions import formatting
from exactly_lib.definitions.current_directory_and_path_type import path_type_path_rendering
from exactly_lib.definitions.entity import concepts
from exactly_lib.definitions.entity import types, syntax_elements
from exactly_lib.definitions.formatting import InstructionName
from exactly_lib.definitions.test_case.instructions import instruction_names
from exactly_lib.help.entities.types.contents_structure import TypeDocumentation
from exactly_lib.type_system.value_type import TypeCategory
from exactly_lib.util.textformat.structure.document import SectionContents
from exactly_lib.util.textformat.textformat_parser import TextParser
_LIST_MAIN_DESCRIPTION_REST = 'Used for argument lists, etc.\n \n \nUseful when the {ATC} is a program with arguments,\nand for the {run} instruction, e.g.\n'
_STRING_MAIN_DESCRIPTION_REST = 'Used for arbitrary string values, and relative file names.\n \n \nWhen used as a relative file name, {POSIX_SYNTAX} should be used.\n'
_TEXT_PARSER = TextParser({'run': InstructionName(instruction_names.RUN_INSTRUCTION_NAME), 
 'POSIX_SYNTAX': POSIX_SYNTAX, 
 'ATC': formatting.concept_(concepts.ACTION_TO_CHECK_CONCEPT_INFO)})
STRING_DOCUMENTATION = TypeDocumentation(TypeCategory.DATA, types.STRING_TYPE_INFO, syntax_elements.STRING_SYNTAX_ELEMENT, _TEXT_PARSER.section_contents(_STRING_MAIN_DESCRIPTION_REST))
LIST_DOCUMENTATION = TypeDocumentation(TypeCategory.DATA, types.LIST_TYPE_INFO, syntax_elements.LIST_SYNTAX_ELEMENT, _TEXT_PARSER.section_contents(_LIST_MAIN_DESCRIPTION_REST))
PATH_DOCUMENTATION = TypeDocumentation(TypeCategory.DATA, types.PATH_TYPE_INFO, syntax_elements.PATH_SYNTAX_ELEMENT, SectionContents([], [
 path_type_path_rendering()]), [
 concepts.TCDS_CONCEPT_INFO.cross_reference_target])