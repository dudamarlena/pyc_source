# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/render/partitioned_entity_set.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 4903 bytes
from typing import List, Callable, Iterable
from exactly_lib.help.contents_structure.entity import HtmlDocHierarchyGeneratorGetter, CliListConstructorGetter, EntityDocumentation
from exactly_lib.help.render import entities_list_renderer
from exactly_lib.help.render.entity_docs import EntitiesListConstructor
from exactly_lib.util.textformat.constructor import sections
from exactly_lib.util.textformat.constructor.section import SectionContentsConstructor, SectionConstructor, ArticleContentsConstructor
from exactly_lib.util.textformat.section_target_hierarchy import hierarchies as h, generator
from exactly_lib.util.textformat.section_target_hierarchy.generator import SectionHierarchyGenerator
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.structure.core import ParagraphItem

class PartitionNamesSetup:

    def __init__(self, local_target_name: str, header: str):
        self.local_target_name = local_target_name
        self.header = header


class PartitionSetup:

    def __init__(self, partition_names_setup: PartitionNamesSetup, filter_entity_docs: Callable[([Iterable[EntityDocumentation]], List[EntityDocumentation])]):
        self.partition_names_setup = partition_names_setup
        self.filter_entity_docs = filter_entity_docs


class EntitiesPartition:

    def __init__(self, partition_names_setup: PartitionNamesSetup, entity_doc_list: List[EntityDocumentation]):
        self.partition_names_setup = partition_names_setup
        self.entity_doc_list = entity_doc_list


def partition_entities(partitions_setup: Iterable[PartitionSetup], entity_doc_list: Iterable[EntityDocumentation]) -> List[EntitiesPartition]:
    ret_val = []
    for partition_setup in partitions_setup:
        entity_docs_in_partition = partition_setup.filter_entity_docs(entity_doc_list)
        if entity_docs_in_partition:
            ret_val.append(EntitiesPartition(partition_setup.partition_names_setup, entity_docs_in_partition))

    return ret_val


class PartitionedCliListConstructorGetter(CliListConstructorGetter):

    def __init__(self, partition_setup_list: Iterable[PartitionSetup], entity_2_summary_paragraphs: Callable[([EntityDocumentation], List[ParagraphItem])]):
        self.partition_setup_list = partition_setup_list
        self.entity_2_summary_paragraphs = entity_2_summary_paragraphs

    def get_constructor--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL              partition_entities
                3  LOAD_DEREF               'self'
                6  LOAD_ATTR                partition_setup_list
                9  LOAD_FAST                'all_entity_doc_list'
               12  CALL_FUNCTION_2       2  '2 positional, 0 named'
               15  STORE_FAST               'partitions'

 L.  67        18  LOAD_GLOBAL              EntitiesPartition
               21  LOAD_GLOBAL              SectionConstructor
               24  LOAD_CONST               ('partition', 'return')
               27  LOAD_CLOSURE             'self'
               30  BUILD_TUPLE_1         1 
               33  LOAD_CODE                <code_object section_constructor>
               36  LOAD_STR                 'PartitionedCliListConstructorGetter.get_constructor.<locals>.section_constructor'
               39  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               45  STORE_FAST               'section_constructor'

 L.  73        48  LOAD_GLOBAL              sections
               51  LOAD_ATTR                contents
               54  LOAD_STR                 'sub_sections'
               57  LOAD_GLOBAL              map
               60  LOAD_FAST                'section_constructor'
               63  LOAD_FAST                'partitions'
               66  CALL_FUNCTION_2       2  '2 positional, 0 named'
               69  CALL_FUNCTION_256   256  '0 positional, 1 named'
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 33


class PartitionedHierarchyGeneratorGetter(HtmlDocHierarchyGeneratorGetter):

    def __init__(self, entity_type_identifier: str, partition_setup_list: Iterable[PartitionSetup], entity_2_article_contents_renderer: Callable[([EntityDocumentation], ArticleContentsConstructor)]):
        self.entity_type_identifier = entity_type_identifier
        self.partition_setup_list = partition_setup_list
        self.entity_2_article_contents_renderer = entity_2_article_contents_renderer

    def get_hierarchy_generator--- This code section failed: ---

 L.  90         0  LOAD_GLOBAL              EntitiesPartition
                3  LOAD_GLOBAL              SectionHierarchyGenerator
                6  LOAD_CONST               ('partition', 'return')
                9  LOAD_CLOSURE             'self'
               12  BUILD_TUPLE_1         1 
               15  LOAD_CODE                <code_object section_hierarchy_node>
               18  LOAD_STR                 'PartitionedHierarchyGeneratorGetter.get_hierarchy_generator.<locals>.section_hierarchy_node'
               21  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               27  STORE_DEREF              'section_hierarchy_node'

 L.  99        30  LOAD_GLOBAL              partition_entities
               33  LOAD_DEREF               'self'
               36  LOAD_ATTR                partition_setup_list
               39  LOAD_FAST                'all_entity_doc_list'
               42  CALL_FUNCTION_2       2  '2 positional, 0 named'
               45  STORE_FAST               'partitions'

 L. 101        48  LOAD_GLOBAL              h
               51  LOAD_ATTR                hierarchy

 L. 102        54  LOAD_GLOBAL              docs
               57  LOAD_ATTR                string_text
               60  LOAD_FAST                'header'
               63  CALL_FUNCTION_1       1  '1 positional, 0 named'
               66  LOAD_STR                 'children'

 L. 104        69  LOAD_CLOSURE             'section_hierarchy_node'
               72  BUILD_TUPLE_1         1 
               75  LOAD_LISTCOMP            '<code_object <listcomp>>'
               78  LOAD_STR                 'PartitionedHierarchyGeneratorGetter.get_hierarchy_generator.<locals>.<listcomp>'
               81  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L. 105        84  LOAD_FAST                'partitions'
               87  GET_ITER         
               88  CALL_FUNCTION_1       1  '1 positional, 0 named'
               91  CALL_FUNCTION_257   257  '1 positional, 1 named'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1