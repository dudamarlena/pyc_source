# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/syntax_elements/objects/integer.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 1356 bytes
from exactly_lib.definitions.cross_ref.name_and_cross_ref import cross_reference_id_list
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.help.entities.syntax_elements.contents_structure import syntax_element_documentation
from exactly_lib.util.textformat.textformat_parser import TextParser
_MAIN_DESCRIPTION_REST = 'A {STRING} that is an expression that evaluates to an integer (using Python syntax).\n\n\nMay be quoted (to allow space).\n\n\n{SYMBOL_REFERENCE_SYNTAX_ELEMENT}s are substituted.\n'
_TEXT_PARSER = TextParser({'STRING': syntax_elements.STRING_SYNTAX_ELEMENT.singular_name, 
 'SYMBOL_REFERENCE_SYNTAX_ELEMENT': syntax_elements.SYMBOL_REFERENCE_SYNTAX_ELEMENT.singular_name})
DOCUMENTATION = syntax_element_documentation(None, syntax_elements.INTEGER_SYNTAX_ELEMENT, _TEXT_PARSER.fnap(_MAIN_DESCRIPTION_REST), [], [], cross_reference_id_list([
 syntax_elements.SYMBOL_REFERENCE_SYNTAX_ELEMENT,
 syntax_elements.STRING_SYNTAX_ELEMENT]))