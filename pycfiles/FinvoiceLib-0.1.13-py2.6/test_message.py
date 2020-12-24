# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/tests/reader/test_message.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.reader.message import Message
from finvoicelib.tests import FinvoiceTestCase

class TestMessage(FinvoiceTestCase):

    def test_usage_no_soap_envelope(self):
        m = Message(None, None)
        m.get_payload()
        return

    def test_usage_no_payload(self):
        m = Message(None, None)
        m.get_payload()
        return