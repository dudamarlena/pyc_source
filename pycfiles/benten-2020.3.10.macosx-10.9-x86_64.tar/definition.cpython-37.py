# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/langserver/definition.py
# Compiled at: 2019-07-19 17:49:40
# Size of source mod 2**32: 527 bytes
"""
textDocument/definition
"""
from .lspobjects import Position
from .base import CWLLangServerBase
import logging
logger = logging.getLogger(__name__)

class Definition(CWLLangServerBase):

    def serve_textDocument_definition(self, client_query):
        params = client_query['params']
        doc_uri = params['textDocument']['uri']
        position = Position(**params['position'])
        doc = self.open_documents[doc_uri]
        return doc.definition(position)