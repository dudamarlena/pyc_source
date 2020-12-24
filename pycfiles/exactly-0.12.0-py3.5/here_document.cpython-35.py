# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/syntax_elements/objects/here_document.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 1420 bytes
from exactly_lib.definitions.cross_ref.name_and_cross_ref import cross_reference_id_list
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.definitions.entity.types import STRING_TYPE_INFO
from exactly_lib.help.entities.syntax_elements.contents_structure import syntax_element_documentation
from exactly_lib.util.textformat.textformat_parser import TextParser
_MAIN_DESCRIPTION_REST = '```\n<<EOF\nfirst line\n...\nlast line\nEOF\n```\n\n\nAny single-word string may be used instead of "EOF" as marker.\nWhat matters is that the maker at start and end of input\nmatches.\n\n\nAny {SYMBOL_REFERENCE_SYNTAX_ELEMENT} appearing in the text is substituted.\n\n'
_TEXT_PARSER = TextParser({'SYMBOL_REFERENCE_SYNTAX_ELEMENT': syntax_elements.SYMBOL_REFERENCE_SYNTAX_ELEMENT.singular_name})
DOCUMENTATION = syntax_element_documentation(None, syntax_elements.HERE_DOCUMENT_SYNTAX_ELEMENT, _TEXT_PARSER.fnap(_MAIN_DESCRIPTION_REST), [], [], cross_reference_id_list([
 STRING_TYPE_INFO,
 syntax_elements.SYMBOL_REFERENCE_SYNTAX_ELEMENT]))