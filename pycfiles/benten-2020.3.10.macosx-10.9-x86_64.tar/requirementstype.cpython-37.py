# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/requirementstype.py
# Compiled at: 2019-09-13 12:05:46
# Size of source mod 2**32: 1085 bytes
from .basetype import CWLBaseType, Intelligence, MapSubjectPredicate
from langserver.lspobjects import Range, CompletionItem
from code.intelligence import LookupNode
from code.intelligencecontext import IntelligenceContext
import logging
logger = logging.getLogger(__name__)

class CWLRequirementsType(CWLBaseType):

    def __init__(self, name, req_types):
        super().__init__(name)
        self.req_types = req_types

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        ln = LookupNode(loc=value_range)
        ln.intelligence_node = self
        code_intel.add_lookup_node(ln)

    def completion(self):
        return [CompletionItem(label=(k.name)) for k in self.req_types]