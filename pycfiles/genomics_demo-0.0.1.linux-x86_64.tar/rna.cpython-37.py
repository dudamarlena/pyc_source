# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nickdg/anaconda3/envs/dna2/lib/python3.7/site-packages/genomics_demo/rna.py
# Compiled at: 2018-10-01 08:57:07
# Size of source mod 2**32: 3920 bytes
complimentary_nucleotides = {'A':'U', 
 'U':'A',  'C':'G',  'G':'C'}
type_motifs = {'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA':'polyA tail mRNA', 
 'GAGAGUA':'clover leaf loop tRNA', 
 'AAGUGC':'microRNA'}

class RNA:

    def __init__(self, sequence: str):
        self.sequence = sequence
        if not self._check_validity():
            raise ValueError('Bad sequence. Sequences must only contain G, C, A, and U')

    def __eq__(self, other):
        if str(self) == str(other):
            return True
        return False

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return "RNA(sequence='{}')".format(self.sequence)

    def _check_validity(self):
        return all((nucleotide in 'GCAU' for nucleotide in self.sequence.upper()))

    def type_rna(self):
        """
        Scans the entire RNA sequence and returns the first motif type
        found from dictionary type_motifs above;
        multiple instances or motifs beyond the first match are not reported
        """
        for index, mo in enumerate(type_motifs):
            if mo in self.sequence.upper():
                return type_motifs[mo]

    def check_polyA(self):
        """
        Checks whether the RNA sequence contains a poly A tail of 50 adenines.
        :return: True if yes, False otherwise
        """
        if self.sequence.endswith('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'):
            return True
        return False

    @property
    def complimentary_sequence(self):
        return RNA(''.join((complimentary_nucleotides[nt.upper()] for nt in self.sequence)))

    @property
    def _check_if_mutated(self):
        """
        This function checks whether the particular sequence inserted corresponds to GGGGGGGGGGUGGGGGGGGG,
        otherwise it means the sequence is mutated and the function reports this.
        :return:
        """
        is_mutated = 'GGGGGGGGGGUGGGGGGGGG' in self.sequence
        print('The fish is mutated') if is_mutated else print('The fish is not mutated')

    def get_aa_sequence(self):
        """
        This function provides the potential amino-acid the RNA sequence encodes, even if this is non-coding RNA.
        :return:
        """
        aa = {'UUU':'Phe', 
         'UUC':'Phe', 
         'UUA':'Leu', 
         'UUG':'Leu', 
         'CUU':'Leu', 
         'CUC':'Leu', 
         'CUA':'Leu', 
         'CUG':'Leu', 
         'AUU':'Ile', 
         'AUC':'Ile', 
         'AUA':'Ile', 
         'AUG':'Met', 
         'GUU':'Val', 
         'GUC':'Val', 
         'GUA':'Val', 
         'GUG':'Val', 
         'UCU':'Ser', 
         'UCC':'Ser', 
         'UCA':'Ser', 
         'UCG':'Ser', 
         'CCU':'Pro', 
         'CCC':'Pro', 
         'CCA':'Pro', 
         'CCG':'Pro', 
         'ACU':'Thr', 
         'ACC':'Thr', 
         'ACA':'Thr', 
         'ACG':'Thr', 
         'GCU':'Ala', 
         'GCC':'Ala', 
         'GCA':'Ala', 
         'UAU':'Tyr', 
         'UAC':'Tyr', 
         'UAA':'Stop', 
         'UAG':'Stop'}
        trunc_sequence = self.sequence[:len(self.sequence) // 3 * 3]
        aa_sequence = [aa[trunc_sequence[i:i + 3:1]] for i in range(0, len(trunc_sequence), 3)]
        return '-'.join(aa_sequence)

    @property
    def reverse_sequence(self):
        return RNA(''.join(reversed(self.sequence)))

    @property
    def rna_start_codon(self):
        """Just a help text"""
        if 'AUG' in self.sequence:
            return 'coding RNA'
        return 'non coding RNA'