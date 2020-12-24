# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/syntax_elements/objects/symbol_name.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 841 bytes
from exactly_lib.definitions import syntax_descriptions
from exactly_lib.definitions.entity import concepts
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.help.entities.syntax_elements.contents_structure import syntax_element_documentation
from exactly_lib.util.textformat.parse import normalize_and_parse
_MAIN_DESCRIPTION_REST = syntax_descriptions.SYMBOL_NAME_SYNTAX_DESCRIPTION
DOCUMENTATION = syntax_element_documentation(None, syntax_elements.SYMBOL_NAME_SYNTAX_ELEMENT, normalize_and_parse(_MAIN_DESCRIPTION_REST), [], [], [
 concepts.SYMBOL_CONCEPT_INFO.cross_reference_target])