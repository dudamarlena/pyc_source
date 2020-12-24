# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/langserver/completion.py
# Compiled at: 2019-08-03 06:58:10
# Size of source mod 2**32: 526 bytes
"""
textDocument/completion
"""
from .lspobjects import Position
from .base import CWLLangServerBase
import logging
logger = logging.getLogger(__name__)

class Completion(CWLLangServerBase):

    def serve_textDocument_completion(self, client_query):
        params = client_query['params']
        doc_uri = params['textDocument']['uri']
        position = Position(**params['position'])
        doc = self.open_documents[doc_uri]
        return doc.completion(position)