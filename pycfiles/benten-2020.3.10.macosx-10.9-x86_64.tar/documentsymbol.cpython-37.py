# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/langserver/documentsymbol.py
# Compiled at: 2019-11-13 20:55:00
# Size of source mod 2**32: 799 bytes
"""
textDocument/documentSymbol
"""
import pathlib, json, hashlib
from .base import CWLLangServerBase
import logging
logger = logging.getLogger(__name__)

class DocumentSymbol(CWLLangServerBase):

    def serve_textDocument_documentSymbol(self, client_query):
        params = client_query['params']
        doc_uri = params['textDocument']['uri']
        doc = self.open_documents[doc_uri]
        self._write_out_graph(doc)
        return doc.symbols

    def _write_out_graph(self, doc):
        graph_data_file = pathlib.Path(self.config.scratch_path, hashlib.md5(doc.doc_uri.encode()).hexdigest() + '.json')
        with graph_data_file.open('w') as (f):
            json.dump((doc.wf_graph), f, indent=2)