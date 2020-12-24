# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/anytype.py
# Compiled at: 2020-02-12 11:03:51
# Size of source mod 2**32: 1097 bytes
from .basetype import CWLBaseType, MapSubjectPredicate, TypeCheck
from .importincludetype import CWLImportInclude
import logging
logger = logging.getLogger(__name__)

class CWLAnyType(CWLBaseType):

    def __init__(self, name, type_dict):
        super().__init__(name)
        self.type_dict = type_dict

    def if_you_can_be_anything_be_this_kind(self, type_name):
        return self.type_dict.get(type_name)

    def all_possible_type_names(self):
        return list(self.type_dict.keys())

    def check(self, node, node_key: str=None, map_sp: MapSubjectPredicate=None) -> TypeCheck:
        if isinstance(node, dict):
            if '$import' in node:
                return TypeCheck(CWLImportInclude(key='$import', import_context=''))
        return TypeCheck(self)