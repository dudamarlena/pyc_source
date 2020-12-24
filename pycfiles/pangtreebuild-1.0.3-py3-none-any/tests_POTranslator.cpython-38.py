# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paulina/pangtree/pangtreebuild/tests/tests_affinity_tree/tests_POTranslator.py
# Compiled at: 2019-12-30 15:48:57
# Size of source mod 2**32: 14688 bytes
import unittest
from ddt import ddt
from pangtreebuild.affinity_tree import poa
from pangtreebuild.pangenome import graph
from pangtreebuild.pangenome.parameters import msa

def nid(x):
    return graph.NodeID(x)


def b(x):
    return graph.Base(x)


@ddt
class PoagraphPOTranslator_read_top_consensus_Test(unittest.TestCase):

    def setUp(self):
        nodes = [
         graph.Node(node_id=(nid(0)), base=(b('T')), aligned_to=None),
         graph.Node(node_id=(nid(1)), base=(b('A')), aligned_to=(nid(2))),
         graph.Node(node_id=(nid(2)), base=(b('G')), aligned_to=(nid(1))),
         graph.Node(node_id=(nid(3)), base=(b('A')), aligned_to=(nid(4))),
         graph.Node(node_id=(nid(4)), base=(b('C')), aligned_to=(nid(3))),
         graph.Node(node_id=(nid(5)), base=(b('A')), aligned_to=(nid(6))),
         graph.Node(node_id=(nid(6)), base=(b('C')), aligned_to=(nid(7))),
         graph.Node(node_id=(nid(7)), base=(b('G')), aligned_to=(nid(8))),
         graph.Node(node_id=(nid(8)), base=(b('T')), aligned_to=(nid(5))),
         graph.Node(node_id=(nid(9)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(10)), base=(b('C')), aligned_to=(nid(11))),
         graph.Node(node_id=(nid(11)), base=(b('T')), aligned_to=(nid(10))),
         graph.Node(node_id=(nid(12)), base=(b('G')), aligned_to=None),
         graph.Node(node_id=(nid(13)), base=(b('A')), aligned_to=(nid(14))),
         graph.Node(node_id=(nid(14)), base=(b('C')), aligned_to=(nid(13)))]
        sequences = {msa.SequenceID('seq0'): graph.Sequence(msa.SequenceID('seq0'), [
                                  graph.SeqPath([*map(nid, [0, 1, 3, 5, 9, 10, 13])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq1'): graph.Sequence(msa.SequenceID('seq1'), [
                                  graph.SeqPath([*map(nid, [1, 3, 6, 9, 11])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq2'): graph.Sequence(msa.SequenceID('seq2'), [
                                  graph.SeqPath([*map(nid, [2, 4, 7, 9, 11, 12])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq3'): graph.Sequence(msa.SequenceID('seq3'), [
                                  graph.SeqPath([*map(nid, [2, 4, 8, 9, 11, 12, 14])])], graph.SequenceMetadata({'group': '1'}))}
        self.poagraph = graph.Poagraph(nodes, sequences)

    def test_read_consensus_path_seq1_only_in_input(self):
        translator = poa._PoagraphPOTranslator(self.poagraph, [
         msa.SequenceID('seq1')])
        _ = translator.get_input_po_content()
        poa_lines = [
         'VERSION=pangenome\n',
         'NAME=pangenome\n',
         'TITLE=pangenome\n',
         'LENGTH=5\n',
         'SOURCECOUNT=2\n',
         'SOURCENAME=seq1\n',
         'SOURCEINFO=5 0 100 0 seq1\n',
         'SOURCENAME=CONSENS0\n',
         'SOURCEINFO=5 0 100 0 CONSENS0\n',
         'a:S0S1\n',
         'a:L0S0S1\n',
         'c:L1S0S1\n',
         'a:L2S0S1\n',
         't:L2S0S1']
        actual_consensus_path = translator.read_consensus_paths(poa_lines, [0])
        expected_consensus_path = [1, 3, 6, 9, 11]
        self.assertEqual(expected_consensus_path, actual_consensus_path[0].path)

    def test_subpoagraph_construction_from_poagraph_keep_seq_0_1(self):
        translator = poa._PoagraphPOTranslator(self.poagraph, [
         msa.SequenceID('seq0'),
         msa.SequenceID('seq1')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = 'VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=9\nSOURCECOUNT=2\nSOURCENAME=seq0\nSOURCEINFO=7 0 0 -1 seq0\nSOURCENAME=seq1\nSOURCEINFO=5 1 100 -1 seq1\nt:S0\na:L0S0S1\na:L1S0S1\na:L2S0A4\nc:L2S1A3\na:L3L4S0S1\nc:L5S0A7\nt:L5S1A6\na:L6S0'
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpoagraph_construction_from_poagraph_keep_seq3(self):
        translator = poa._PoagraphPOTranslator(self.poagraph, [
         msa.SequenceID('seq3')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = 'VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=7\nSOURCECOUNT=1\nSOURCENAME=seq3\nSOURCEINFO=7 0 100 -1 seq3\ng:S0\nc:L0S0\nt:L1S0\na:L2S0\nt:L3S0\ng:L4S0\nc:L5S0'
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpoagraph_construction_full_graph(self):
        nodes = [
         graph.Node(node_id=(nid(0)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(1)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(2)), base=(b('C')), aligned_to=None),
         graph.Node(node_id=(nid(3)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(4)), base=(b('T')), aligned_to=None)]
        sequences = {msa.SequenceID('seq0'): graph.Sequence(msa.SequenceID('seq0'), [
                                  graph.SeqPath([*map(nid, [0, 1, 2, 3, 4])])], graph.SequenceMetadata({'group': '1'}))}
        poagraph = graph.Poagraph(nodes, sequences)
        translator = poa._PoagraphPOTranslator(poagraph, [msa.SequenceID('seq0')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = 'VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=5\nSOURCECOUNT=1\nSOURCENAME=seq0\nSOURCEINFO=5 0 100 -1 seq0\na:S0\na:L0S0\nc:L1S0\na:L2S0\nt:L3S0'
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpoagraph_should_omit_edges_1(self):
        nodes = [
         graph.Node(node_id=(nid(0)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(1)), base=(b('C')), aligned_to=None),
         graph.Node(node_id=(nid(2)), base=(b('C')), aligned_to=None)]
        sequences = {msa.SequenceID('seq1'): graph.Sequence(msa.SequenceID('seq1'), [
                                  graph.SeqPath([*map(nid, [0, 2])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq2'): graph.Sequence(msa.SequenceID('seq2'), [
                                  graph.SeqPath([*map(nid, [0, 1, 2])])], graph.SequenceMetadata({'group': '1'}))}
        poagraph = graph.Poagraph(nodes, sequences)
        translator = poa._PoagraphPOTranslator(poagraph, [msa.SequenceID('seq2')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = 'VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=3\nSOURCECOUNT=1\nSOURCENAME=seq2\nSOURCEINFO=3 0 100 -1 seq2\na:S0\nc:L0S0\nc:L1S0'
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpoagraph_should_omit_edges_2(self):
        nodes = [
         graph.Node(node_id=(nid(0)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(1)), base=(b('C')), aligned_to=None),
         graph.Node(node_id=(nid(2)), base=(b('C')), aligned_to=None)]
        sequences = {msa.SequenceID('seq1'): graph.Sequence(msa.SequenceID('seq1'), [
                                  graph.SeqPath([*map(nid, [0, 2])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq2'): graph.Sequence(msa.SequenceID('seq2'), [
                                  graph.SeqPath([*map(nid, [0, 1, 2])])], graph.SequenceMetadata({'group': '1'}))}
        poagraph = graph.Poagraph(nodes, sequences)
        translator = poa._PoagraphPOTranslator(poagraph, [msa.SequenceID('seq1')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = 'VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=2\nSOURCECOUNT=1\nSOURCENAME=seq1\nSOURCEINFO=2 0 100 -1 seq1\na:S0\nc:L0S0'
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpoagraph_should_omit_in_nodes_and_aligned_nodes(self):
        nodes = [
         graph.Node(node_id=(nid(0)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(1)), base=(b('C')), aligned_to=(nid(2))),
         graph.Node(node_id=(nid(2)), base=(b('T')), aligned_to=(nid(1))),
         graph.Node(node_id=(nid(3)), base=(b('G')), aligned_to=None)]
        sequences = {msa.SequenceID('seq1'): graph.Sequence(msa.SequenceID('seq1'), [
                                  graph.SeqPath([*map(nid, [0, 1, 3])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq2'): graph.Sequence(msa.SequenceID('seq2'), [
                                  graph.SeqPath([*map(nid, [0, 2, 3])])], graph.SequenceMetadata({'group': '1'}))}
        poagraph = graph.Poagraph(nodes, sequences)
        translator = poa._PoagraphPOTranslator(poagraph, [msa.SequenceID('seq2')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = 'VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=3\nSOURCECOUNT=1\nSOURCENAME=seq2\nSOURCEINFO=3 0 100 -1 seq2\na:S0\nt:L0S0\ng:L1S0'
        self.assertEqual(expected_po_content, actual_po_content)

    def test_subpoagraph_unfilled_nodes(self):
        symbol_for_uknown = '?'
        nodes = [graph.Node(node_id=(nid(0)), base=(b('A')), aligned_to=(nid(1))),
         graph.Node(node_id=(nid(1)), base=(b('C')), aligned_to=(nid(0))),
         graph.Node(node_id=(nid(2)), base=(b('G')), aligned_to=None),
         graph.Node(node_id=(nid(3)), base=(b(symbol_for_uknown)), aligned_to=None),
         graph.Node(node_id=(nid(4)), base=(b(symbol_for_uknown)), aligned_to=None),
         graph.Node(node_id=(nid(5)), base=(b('G')), aligned_to=None),
         graph.Node(node_id=(nid(6)), base=(b('C')), aligned_to=None),
         graph.Node(node_id=(nid(7)), base=(b('A')), aligned_to=None),
         graph.Node(node_id=(nid(5)), base=(b('T')), aligned_to=None)]
        sequences = {msa.SequenceID('seq1'): graph.Sequence(msa.SequenceID('seq1'), [
                                  graph.SeqPath([*map(nid, [0, 2, 3, 4, 7, 8])])], graph.SequenceMetadata({'group': '1'})), 
         
         msa.SequenceID('seq2'): graph.Sequence(msa.SequenceID('seq2'), [
                                  graph.SeqPath([*map(nid, [1, 2, 5, 6, 7, 8])])], graph.SequenceMetadata({'group': '1'}))}
        poagraph = graph.Poagraph(nodes, sequences)
        translator = poa._PoagraphPOTranslator(poagraph, [msa.SequenceID('seq1'),
         msa.SequenceID('seq2')])
        actual_po_content = translator.get_input_po_content()
        expected_po_content = f"VERSION=pangenome\nNAME=pangenome\nTITLE=pangenome\nLENGTH=9\nSOURCECOUNT=2\nSOURCENAME=seq1\nSOURCEINFO=6 0 100 -1 seq1\nSOURCENAME=seq2\nSOURCEINFO=6 1 100 -1 seq2\na:S0A1\nc:S1A0\ng:L0L1S0S1\n{symbol_for_uknown}:L2S0\n{symbol_for_uknown}:L3S0\ng:L2S1\nc:L5S1\na:L4L6S0S1\nt:L7S0S1"
        self.assertEqual(expected_po_content, actual_po_content)