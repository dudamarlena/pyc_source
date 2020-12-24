# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/tests/unit/blast/results/pointfinder/test_PlasmidfinderHitHSP.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 4096 bytes
import unittest
import staramr.blast.results.plasmidfinder.PlasmidfinderHitHSP as PlasmidfinderHitHSP

class PlasmidfinderHitHSPTest(unittest.TestCase):

    def testParseSequenceId1(self):
        test_blast_record = {'sstart':20, 
         'send':30,  'sstrand':'ABC',  'qstart':1,  'qend':10,  'qseqid':'RepA_1_pKPC-CAV1321_CP011611'}
        plasmid_hit_hsp = PlasmidfinderHitHSP('test_file', test_blast_record)
        self.assertEqual('RepA', plasmid_hit_hsp.get_amr_gene_name(), 'Did not parse correct gene name')
        self.assertEqual('1', plasmid_hit_hsp.get_amr_gene_variant(), 'Did not parse correct gene variant')
        self.assertEqual('RepA_1', plasmid_hit_hsp.get_amr_gene_name_with_variant(), 'Did not parse correct gene name variant')
        self.assertEqual('CP011611', plasmid_hit_hsp.get_amr_gene_accession(), 'Did not parse correct gene name variant')
        self.assertEqual('RepA_1_CP011611', plasmid_hit_hsp.get_amr_gene_variant_accession(), 'Did not parse correct gene name variant accession')

    def testParseSequenceId2(self):
        test_blast_record = {'sstart':20, 
         'send':30,  'sstrand':'ABC',  'qstart':1,  'qend':10,  'qseqid':'IncHI2_1__BX664015'}
        plasmid_hit_hsp = PlasmidfinderHitHSP('test_file', test_blast_record)
        self.assertEqual('IncHI2', plasmid_hit_hsp.get_amr_gene_name(), 'Did not parse correct gene name')
        self.assertEqual('1', plasmid_hit_hsp.get_amr_gene_variant(), 'Did not parse correct gene variant')
        self.assertEqual('IncHI2_1', plasmid_hit_hsp.get_amr_gene_name_with_variant(), 'Did not parse correct gene name variant')
        self.assertEqual('BX664015', plasmid_hit_hsp.get_amr_gene_accession(), 'Did not parse correct gene name variant')
        self.assertEqual('IncHI2_1_BX664015', plasmid_hit_hsp.get_amr_gene_variant_accession(), 'Did not parse correct gene name variant accession')

    def testParseSequenceId3(self):
        test_blast_record = {'sstart':20, 
         'send':30,  'sstrand':'ABC',  'qstart':1,  'qend':10,  'qseqid':'IncB/O/K/Z_1__CU928147'}
        plasmid_hit_hsp = PlasmidfinderHitHSP('test_file', test_blast_record)
        self.assertEqual('IncB/O/K/Z', plasmid_hit_hsp.get_amr_gene_name(), 'Did not parse correct gene name')
        self.assertEqual('1', plasmid_hit_hsp.get_amr_gene_variant(), 'Did not parse correct gene variant')
        self.assertEqual('IncB/O/K/Z_1', plasmid_hit_hsp.get_amr_gene_name_with_variant(), 'Did not parse correct gene name variant')
        self.assertEqual('CU928147', plasmid_hit_hsp.get_amr_gene_accession(), 'Did not parse correct gene name variant')
        self.assertEqual('IncB/O/K/Z_1_CU928147', plasmid_hit_hsp.get_amr_gene_variant_accession(), 'Did not parse correct gene name variant accession')

    def testParseSequenceId4(self):
        test_blast_record = {'sstart':20, 
         'send':30,  'sstrand':'ABC',  'qstart':1,  'qend':10,  'qseqid':'IncFII(Serratia)_1_Serratia_NC_009829'}
        plasmid_hit_hsp = PlasmidfinderHitHSP('test_file', test_blast_record)
        self.assertEqual('IncFII(Serratia)', plasmid_hit_hsp.get_amr_gene_name(), 'Did not parse correct gene name')
        self.assertEqual('1', plasmid_hit_hsp.get_amr_gene_variant(), 'Did not parse correct gene variant')
        self.assertEqual('IncFII(Serratia)_1', plasmid_hit_hsp.get_amr_gene_name_with_variant(), 'Did not parse correct gene name variant')
        self.assertEqual('NC_009829', plasmid_hit_hsp.get_amr_gene_accession(), 'Did not parse correct gene name variant')
        self.assertEqual('IncFII(Serratia)_1_NC_009829', plasmid_hit_hsp.get_amr_gene_variant_accession(), 'Did not parse correct gene name variant accession')