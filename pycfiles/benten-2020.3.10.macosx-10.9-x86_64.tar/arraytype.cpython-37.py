# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/arraytype.py
# Compiled at: 2020-03-10 07:39:54
# Size of source mod 2**32: 1632 bytes
from .basetype import CWLBaseType, Intelligence, MapSubjectPredicate, TypeCheck, Match
from langserver.lspobjects import Range
from code.intelligencecontext import IntelligenceContext
from .typeinference import infer_type
from .lib import get_range_for_value

class CWLArrayType(CWLBaseType):

    def __init__(self, name, allowed_types):
        super().__init__(name)
        if not isinstance(allowed_types, list):
            allowed_types = [
             allowed_types]
        self.types = allowed_types

    def check(self, node, node_key: str=None, map_sp: MapSubjectPredicate=None) -> TypeCheck:
        if isinstance(node, list):
            return TypeCheck(self)
        return TypeCheck(self, match=(Match.No))

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        if not isinstance(node, list):
            return
        for n, v in enumerate(node):
            inferred_type = infer_type(v, self.types)
            inferred_type.parse(doc_uri=doc_uri,
              node=v,
              intel_context=intel_context,
              code_intel=code_intel,
              problems=problems,
              value_range=(get_range_for_value(node, n)),
              requirements=requirements)