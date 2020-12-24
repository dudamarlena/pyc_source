# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/utils/test__txs.py
# Compiled at: 2020-03-24 14:57:35
# Size of source mod 2**32: 929 bytes
import unittest
from ddgen.utils import prioritize_refseq_transcripts

class TestTranscripts(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_min_transcripts(self):
        txs = [
         'NM_123.4', 'NM_124.4', 'NM_1001.2']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'NM_123.4')

    def test_min_transcripts_multiple_sources(self):
        txs = [
         'NM_123.4', 'NR_123.4', 'XM_123.4', 'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'NM_123.4')
        txs = [
         'NR_123.4', 'XM_123.4', 'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'XM_123.4')
        txs = [
         'NR_123.4', 'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'NR_123.4')
        txs = [
         'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'XR_123.4')