# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/parameter/genomictagoption.py
# Compiled at: 2014-07-07 15:44:50
from option import Option

class GenomicTagOption(Option):

    def __init__(self, *args, **kwargs):
        self.valid_keys = [
         '-10_signal', '-35_signal', "3'UTR", "5'UTR",
         'CAAT_signal', 'CDS', 'C_region', 'D-loop',
         'D_segment', 'GC_signal', 'J_segment', 'LTR',
         'N_region', 'RBS', 'STS', 'S_region', 'TATA_signal',
         'V_region', 'V_segment', 'assembly_gap',
         'attenuator', 'enhancer', 'exon', 'gap', 'gene',
         'iDNA', 'intron', 'mRNA', 'mat_peptide', 'misc_RNA',
         'misc_binding', 'misc_difference', 'misc_feature',
         'misc_recomb', 'misc_signal', 'misc_structure',
         'mobile_element', 'modified_base', 'ncRNA',
         'old_sequence', 'operon', 'oriT', 'polyA_signal',
         'polyA_site', 'precursor_RNA', 'prim_transcript',
         'primer_bind', 'promoter', 'protein_bind', 'rRNA',
         'rep_origin', 'repeat_region', 'sig_peptide',
         'source', 'stem_loop', 'tRNA', 'terminator',
         'tmRNA', 'transit_peptide', 'unsure', 'variation',
         'whole', 'all']
        self.validKeySet = {x:x for x in sorted(self.valid_keys)}
        kwargs['options'] = self.validKeySet
        Option.__init__(self, *args, **kwargs)