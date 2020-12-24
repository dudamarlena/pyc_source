# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/helper/generate_constraint.py
# Compiled at: 2019-09-03 03:37:41
# Size of source mod 2**32: 992 bytes
import collections
from typing import List, Dict
from tokenizer_tools.tagset.offset.corpus import Corpus

def generate_constraint(corpus: Corpus, output_attr: str=None) -> Dict[(str, List[str])]:
    domain_list = collections.defaultdict(set)
    for item in corpus:
        if output_attr == 'label':
            domain = item.label
        else:
            domain = item.extra_attr[output_attr]
        entity_list = []
        for span in item.span_set:
            entity = span.entity
            entity_list.append(entity)

        domain_list[domain].update(entity_list)

    domain_mapping = dict()
    sorted_domain_list = sorted((domain_list.items()), key=(lambda x: x[0]))
    for k, v in sorted_domain_list:
        sorted_entity_list = list(sorted(v))
        domain_mapping[k] = sorted_entity_list

    return domain_mapping