# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/code/intelligence.py
# Compiled at: 2020-03-10 08:45:40
# Size of source mod 2**32: 2464 bytes
"""Provides classes that can be used to infer document location
from cursor location and provide auto-completions.

Language Model objects parse the document to produce document
model objects.

For details see ../../docs/document-model.md
"""
from typing import List
import pathlib
from langserver.lspobjects import Position, Range, CompletionItem, Hover
from .executioncontext import ExecutionContext
import logging
logger = logging.getLogger(__name__)

class LookupNode:

    def __init__(self, loc: Range):
        self.loc = loc
        self.intelligence_node = None


class IntelligenceNode:

    def __init__(self, completions: List[str]=None, doc: str=''):
        self._completions = completions or []
        self.doc = doc

    def completion(self):
        return [CompletionItem(label=c) for c in self._completions]

    def hover(self):
        return Hover((self.doc), is_markdown=True)

    def definition(self):
        pass


class Intelligence:

    def __init__(self):
        self.lookup_table = []
        self.type_defs = {}
        self.namespaces = {}
        self.execution_context = None

    def add_lookup_node(self, node: LookupNode):
        self.lookup_table.append(node)

    def load_namespaces(self, cwl: dict):
        if '$namespaces' in cwl:
            self.namespaces = cwl['$namespaces']

    def prepare_execution_context(self, doc_uri: str, cwl: dict, scratch_path: pathlib.Path):
        self.execution_context = ExecutionContext(doc_uri=doc_uri,
          scratch_path=scratch_path,
          cwl=cwl,
          user_types=(self.type_defs))

    def prepare_expression_lib(self, expression_lib: list):
        self.execution_context.set_expression_lib(expression_lib)

    def get_doc_element(self, loc: Position):
        for n in self.lookup_table:
            if n.loc.start.line <= loc.line <= n.loc.end.line:
                if loc.line > n.loc.start.line or loc.character >= n.loc.start.character:
                    if loc.line < n.loc.end.line or loc.character <= n.loc.end.character:
                        return n.intelligence_node