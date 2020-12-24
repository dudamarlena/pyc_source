# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/reader/message.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements.finvoice_root import FinvoiceRoot
from finvoicelib.soap_envelope import SoapEnvelope

class Message(object):
    errors = None
    envelope_tree = None
    payload_tree = None

    def __init__(self, payload_tree, envelope_tree):
        self.errors = []
        self.payload_tree = payload_tree
        self.envelope_tree = envelope_tree

    def get_envelope(self):
        if not self.envelope_tree:
            return None
        else:
            soap = SoapEnvelope(self.envelope_tree)
            return soap

    def get_payload(self):
        if not self.payload_tree:
            return None
        else:
            f = FinvoiceRoot('Finvoice')
            f.build(self.payload_tree)
            f.errors = self.errors + f.errors
            return f