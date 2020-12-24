# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/types/all_types.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1058 bytes
from typing import List
from exactly_lib.help.entities.types.contents_structure import TypeDocumentation
from exactly_lib.help.entities.types.objects import data_types, logic_types
from exactly_lib.type_system.value_type import TypeCategory

def all_types() -> List[TypeDocumentation]:
    return [
     data_types.STRING_DOCUMENTATION,
     data_types.LIST_DOCUMENTATION,
     data_types.PATH_DOCUMENTATION,
     logic_types.LINE_MATCHER_DOCUMENTATION,
     logic_types.FILE_MATCHER_DOCUMENTATION,
     logic_types.FILES_MATCHER_DOCUMENTATION,
     logic_types.STRING_MATCHER_DOCUMENTATION,
     logic_types.STRING_TRANSFORMER_DOCUMENTATION,
     logic_types.PROGRAM_DOCUMENTATION]


NAME_2_TYPE_DOC = dict(map(lambda x: (x.singular_name(), x), all_types()))

def type_docs_of_type_category(category: TypeCategory, type_docs: List[TypeDocumentation]) -> List[TypeDocumentation]:
    return list(filter(lambda type_doc: type_doc.type_category is category, type_docs))