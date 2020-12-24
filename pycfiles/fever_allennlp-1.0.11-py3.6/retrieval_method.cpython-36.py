# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fever/evidence/retrieval_methods/retrieval_method.py
# Compiled at: 2019-02-21 15:52:13
# Size of source mod 2**32: 297 bytes
from allennlp.common import Registrable
from fever.reader import FEVERDocumentDatabase

class RetrievalMethod(Registrable):

    def __init__(self, database: FEVERDocumentDatabase):
        self.database = database

    def get_sentences_for_claim(self, claim_text, include_text=False):
        pass