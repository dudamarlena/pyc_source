# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellexer/summarizer/interface.py
# Compiled at: 2018-08-28 13:07:16
# Size of source mod 2**32: 821 bytes
from collections import namedtuple
Document = namedtuple('Document', ('id', 'size', 'title', 'url', 'error', 'size_format'))
Item = namedtuple('Item', ('text', 'rank', 'weight'))
ConceptTree = namedtuple('ConceptTree', ('children', 'main_pharse', 'sentence_ids',
                                         'status', 'text', 'weight'))
SummarizeResult = namedtuple('SummarizeResult', ('document', 'structure', 'topics',
                                                 'items', 'total_items_count', 'concept_tree',
                                                 'named_entity_tree'))
MultiSummarizeResult = namedtuple('MultiSummarizeResult', ('documents', 'structure',
                                                           'topics', 'items', 'concept_tree',
                                                           'named_entity_tree', 'related_facts_query',
                                                           'related_facts_tree'))