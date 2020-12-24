# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/common/render_syntax_contents.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 4449 bytes
from typing import Iterable, List, Sequence, Optional
from exactly_lib.common.help.syntax_contents_structure import InvokationVariant, SyntaxElementDescription
from exactly_lib.definitions import doc_format
from exactly_lib.definitions.doc_format import syntax_text
from exactly_lib.help import std_tags
from exactly_lib.util.textformat.structure import document as doc, lists
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.structure.core import ParagraphItem
_SYNTAX_LINE_TAGS = frozenset([std_tags.SYNTAX_TEXT])
LIST_INDENT = 2
BLANK_LINE_BETWEEN_ELEMENTS = lists.Separations(1, 0)

def variants_list(instruction_name: str, invokation_variants: Iterable[InvokationVariant], indented: bool=False,
                  custom_separations: lists.Separations=None) -> ParagraphItem:
    title_prefix = instruction_name + ' ' if instruction_name else ''
    items = []
    for x in invokation_variants:
        assert isinstance(x, InvokationVariant)
        title = title_prefix + x.syntax
        items.append(docs.list_item(syntax_text(title), list(x.description_rest)))

    return lists.HeaderContentList(items, lists.Format(lists.ListType.VARIABLE_LIST, custom_indent_spaces=_custom_list_indent(indented), custom_separations=custom_separations))


def invokation_variants_paragraphs--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              ParagraphItem
                3  LOAD_CONST               ('return',)
                6  LOAD_CLOSURE             'syntax_element_descriptions'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object syntax_element_description_list>
               15  LOAD_STR                 'invokation_variants_paragraphs.<locals>.syntax_element_description_list'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_DEREF              'syntax_element_description_list'

 L.  58        27  LOAD_GLOBAL              List
               30  LOAD_GLOBAL              ParagraphItem
               33  BINARY_SUBSCR    
               34  LOAD_CONST               ('return',)
               37  LOAD_CLOSURE             'syntax_element_description_list'
               40  LOAD_CLOSURE             'syntax_element_descriptions'
               43  BUILD_TUPLE_2         2 
               46  LOAD_CODE                <code_object syntax_element_description_paragraph_items>
               49  LOAD_STR                 'invokation_variants_paragraphs.<locals>.syntax_element_description_paragraph_items'
               52  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               58  STORE_FAST               'syntax_element_description_paragraph_items'

 L.  65        61  LOAD_FAST                'invokation_variants'
               64  UNARY_NOT        
               65  POP_JUMP_IF_FALSE    72  'to 72'

 L.  66        68  BUILD_LIST_0          0 
               71  RETURN_END_IF    
             72_0  COME_FROM            65  '65'

 L.  67        72  LOAD_GLOBAL              variants_list
               75  LOAD_FAST                'instruction_name_or_none'

 L.  68        78  LOAD_FAST                'invokation_variants'
               81  LOAD_STR                 'custom_separations'

 L.  69        84  LOAD_GLOBAL              docs
               87  LOAD_ATTR                SEPARATION_OF_HEADER_AND_CONTENTS
               90  CALL_FUNCTION_258   258  '2 positional, 1 named'
               93  BUILD_LIST_1          1 

 L.  70        96  LOAD_FAST                'syntax_element_description_paragraph_items'
               99  CALL_FUNCTION_0       0  '0 positional, 0 named'
              102  BINARY_ADD       
              103  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def invokation_variants_content(instruction_name: Optional[str], invokation_variants: Sequence[InvokationVariant], syntax_element_descriptions: Iterable[SyntaxElementDescription]) -> doc.SectionContents:
    return doc.SectionContents(invokation_variants_paragraphs(instruction_name, invokation_variants, syntax_element_descriptions), [])


_WHERE_PARA = docs.para(doc_format.text_as_header('where'))
FORMS_PARA = docs.para(doc_format.text_as_header('Forms:'))

def _custom_list_indent(indented: bool) -> int:
    if indented:
        return
    return 0