# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/basetype.py
# Compiled at: 2020-03-10 08:45:40
# Size of source mod 2**32: 1288 bytes
from dataclasses import dataclass
from enum import IntEnum
from langserver.lspobjects import Range
from code.intelligence import IntelligenceNode, Intelligence
from code.intelligencecontext import IntelligenceContext

class MapSubjectPredicate:

    def __init__(self, subject, predicate):
        self.subject = subject
        self.predicate = predicate


class Match(IntEnum):
    Yes = 0
    Maybe = 1
    No = 2


@dataclass
class TypeCheck:
    cwl_type: 'CWLBaseType'
    match = Match.Yes
    match: Match
    missing_req_fields = None
    missing_req_fields: list
    missing_opt_fields = None
    missing_opt_fields: list


class CWLBaseType(IntelligenceNode):

    def __init__(self, name, doc=''):
        super().__init__(doc=doc)
        self.name = name

    def check(self, node, node_key: str=None, map_sp: MapSubjectPredicate=None) -> TypeCheck:
        pass

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        pass