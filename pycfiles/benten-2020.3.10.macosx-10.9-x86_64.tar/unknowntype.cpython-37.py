# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/unknowntype.py
# Compiled at: 2019-08-22 17:10:49
# Size of source mod 2**32: 1062 bytes
from .basetype import CWLBaseType, MapSubjectPredicate
from code.workflow import Workflow
from code.intelligence import Intelligence
from langserver.lspobjects import Range, Diagnostic, DiagnosticSeverity
import logging
logger = logging.getLogger(__name__)

class CWLUnknownType(CWLBaseType):

    def __init__(self, name, expected):
        super().__init__(name)
        self.expected = expected

    def parse(self, doc_uri: str, node, intel_context: Workflow, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        problems += [
         Diagnostic(_range=value_range,
           message=f"Got type {self.name}. Expecting one of {self.expected}",
           severity=(DiagnosticSeverity.Error))]