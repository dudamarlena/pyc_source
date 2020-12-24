# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/section_target_hierarchy/table_of_contents.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 914 bytes
from typing import Sequence
from exactly_lib.util.textformat.section_target_hierarchy.targets import TargetInfoNode
from exactly_lib.util.textformat.structure import core as doc
from exactly_lib.util.textformat.structure import lists
from exactly_lib.util.textformat.structure import structures as docs

def toc_list(target_info_hierarchy: Sequence[TargetInfoNode], list_type: lists.ListType) -> doc.ParagraphItem:
    items = []
    for node in target_info_hierarchy:
        sub_lists = []
        if node.children:
            sub_lists = [
             toc_list(node.children, list_type)]
        item = docs.list_item(docs.cross_reference(node.data.presentation_text, node.data.target), sub_lists)
        items.append(item)

    return lists.HeaderContentList(items, lists.Format(list_type))