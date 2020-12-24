# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/render/entities_list_renderer.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 2461 bytes
"""
Utilities for generating documentation for "entities" - things with a name and single-line-description.

Makes it possible to reuse some code for generating documentation.
"""
from typing import List, Callable
from exactly_lib.help import std_tags
from exactly_lib.help.contents_structure.entity import EntityDocumentation, HtmlDocHierarchyGeneratorGetter
from exactly_lib.help.render.entity_docs import sorted_entity_list
from exactly_lib.util.textformat.constructor import paragraphs
from exactly_lib.util.textformat.constructor.section import ArticleContentsConstructor
from exactly_lib.util.textformat.section_target_hierarchy import hierarchies as h
from exactly_lib.util.textformat.section_target_hierarchy.generator import SectionHierarchyGenerator

class FlatEntityListHierarchyGeneratorGetter(HtmlDocHierarchyGeneratorGetter):

    def __init__(self, entity_type_identifier: str, mk_article_constructor: Callable[([EntityDocumentation], ArticleContentsConstructor)]):
        self._entity_type_identifier = entity_type_identifier
        self._mk_article_constructor = mk_article_constructor

    def get_hierarchy_generator(self, header: str, all_entity_doc_list: List[EntityDocumentation]) -> SectionHierarchyGenerator:
        return entity_list_hierarchy(self._entity_type_identifier, self._mk_article_constructor, header, all_entity_doc_list)


def entity_list_hierarchy--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              EntityDocumentation
                3  LOAD_GLOBAL              SectionHierarchyGenerator
                6  LOAD_CONST               ('entity', 'return')
                9  LOAD_CLOSURE             'entity_type_identifier'
               12  LOAD_CLOSURE             'mk_article_constructor'
               15  BUILD_TUPLE_2         2 
               18  LOAD_CODE                <code_object entity_node>
               21  LOAD_STR                 'entity_list_hierarchy.<locals>.entity_node'
               24  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               30  STORE_DEREF              'entity_node'

 L.  54        33  LOAD_GLOBAL              h
               36  LOAD_ATTR                hierarchy

 L.  55        39  LOAD_FAST                'header'

 L.  56        42  LOAD_GLOBAL              paragraphs
               45  LOAD_ATTR                empty
               48  CALL_FUNCTION_0       0  '0 positional, 0 named'

 L.  58        51  LOAD_CLOSURE             'entity_node'
               54  BUILD_TUPLE_1         1 
               57  LOAD_LISTCOMP            '<code_object <listcomp>>'
               60  LOAD_STR                 'entity_list_hierarchy.<locals>.<listcomp>'
               63  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L.  59        66  LOAD_GLOBAL              sorted_entity_list
               69  LOAD_FAST                'entities'
               72  CALL_FUNCTION_1       1  '1 positional, 0 named'
               75  GET_ITER         
               76  CALL_FUNCTION_1       1  '1 positional, 0 named'
               79  CALL_FUNCTION_3       3  '3 positional, 0 named'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1