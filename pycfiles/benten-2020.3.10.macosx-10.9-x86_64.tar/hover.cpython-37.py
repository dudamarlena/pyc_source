# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/langserver/hover.py
# Compiled at: 2019-10-23 15:03:01
# Size of source mod 2**32: 505 bytes
"""
textDocument/hover
"""
from .lspobjects import Position
from .base import CWLLangServerBase
import logging
logger = logging.getLogger(__name__)

class Hover(CWLLangServerBase):

    def serve_textDocument_hover(self, client_query):
        params = client_query['params']
        doc_uri = params['textDocument']['uri']
        position = Position(**params['position'])
        doc = self.open_documents[doc_uri]
        return doc.hover(position)