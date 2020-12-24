# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/importincludetype.py
# Compiled at: 2020-02-12 11:03:51
# Size of source mod 2**32: 2174 bytes
"""Represents an $include or $import"""
from .basetype import CWLBaseType, IntelligenceContext, Intelligence, MapSubjectPredicate
from .linkedfiletype import CWLLinkedFile
from .linkedschemadeftype import CWLLinkedSchemaDef
from langserver.lspobjects import Diagnostic, DiagnosticSeverity, Range
from .lib import get_range_for_key, get_range_for_value

class CWLImportInclude(CWLBaseType):

    def __init__(self, key, import_context):
        super().__init__('Import/Include')
        self.key = key
        self.import_context = import_context

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        if len(node) > 1:
            problems += [
             Diagnostic(_range=value_range,
               message=f"{self.key} has to be the only key",
               severity=(DiagnosticSeverity.Error))]
            return
        if self.import_context == 'InputRecordSchema':
            if self.key != '$import':
                problems += [
                 Diagnostic(_range=value_range,
                   message='Expecting an $import',
                   severity=(DiagnosticSeverity.Error))]
                return
            inferred_type = CWLLinkedSchemaDef(prefix=(node.get('$import')))
        else:
            inferred_type = CWLLinkedFile(prefix=(node.get(self.key)))
        inferred_type.parse(doc_uri=doc_uri,
          node=(node.get(self.key)),
          intel_context=intel_context,
          code_intel=code_intel,
          problems=problems,
          node_key=(self.key),
          map_sp=map_sp,
          key_range=key_range,
          value_range=(get_range_for_value(node, self.key)),
          requirements=requirements)