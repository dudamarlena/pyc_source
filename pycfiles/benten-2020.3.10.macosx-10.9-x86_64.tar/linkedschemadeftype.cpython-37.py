# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/linkedschemadeftype.py
# Compiled at: 2020-02-12 11:03:51
# Size of source mod 2**32: 1795 bytes
"""Types are stored in the code_intel type dictionary. They are keyed by the URI (if off-disk) or
 the relative path if on-disk. When matching types the path is normalized. The reason why we store
 the relative path is that it makes for a better looking auto-completion."""
import pathlib
from urllib.parse import urlparse
from .linkedfiletype import CWLLinkedFile
from .basetype import IntelligenceContext, Intelligence, MapSubjectPredicate
from langserver.lspobjects import Diagnostic, DiagnosticSeverity, Range
import logging
logger = logging.getLogger(__name__)

class CWLLinkedSchemaDef(CWLLinkedFile):

    def parse(self, doc_uri, node, intel_context, code_intel, problems, node_key=None, map_sp=None, key_range=None, value_range=None, requirements=None):
        super().parse(doc_uri, node, intel_context, code_intel, problems, node_key, map_sp, key_range, value_range, requirements)
        if isinstance(self.node_dict, list):
            _type_list = self.node_dict
        else:
            if isinstance(self.node_dict, dict):
                _type_list = [
                 self.node_dict]
            else:
                problems += [
                 Diagnostic(_range=value_range,
                   message='Problem parsing SchemaDef file',
                   severity=(DiagnosticSeverity.Error))]
                return
        for _type in _type_list:
            if 'name' in _type:
                name = self.prefix + '#' + _type.pop('name')
                code_intel.type_defs[name] = _type