# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/namespacedtype.py
# Compiled at: 2019-10-23 15:03:01
# Size of source mod 2**32: 1167 bytes
from .basetype import CWLBaseType, MapSubjectPredicate
from code.intelligence import Intelligence
from code.intelligencecontext import IntelligenceContext
from langserver.lspobjects import Range, Diagnostic, DiagnosticSeverity
import logging
logger = logging.getLogger(__name__)

class CWLNameSpacedType(CWLBaseType):

    def __init__(self, name):
        super().__init__(name)

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        _s = self.name.split(':')
        if _s[0] not in code_intel.namespaces:
            problems += [
             Diagnostic(_range=(key_range or value_range),
               message=f"Expecting one of: {sorted(code_intel.namespaces)}",
               severity=(DiagnosticSeverity.Error))]