# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nickdg/anaconda3/envs/dna2/lib/python3.7/site-packages/genomics_demo/dna.py
# Compiled at: 2018-10-01 10:12:01
# Size of source mod 2**32: 2919 bytes
complimentary_nucleotides = {'A':'T', 
 'T':'A',  'C':'G',  'G':'C'}

class DNA:

    def __init__(self, sequence: str):
        """

        :param sequence: A string representing GCTA nucleotides.
        """
        self.sequence = sequence
        if not self._check_validity():
            raise ValueError('Bad sequence. Sequences must only contain G, C, A, and T')

    def __eq__(self, other):
        if str(self) == str(other):
            return True
        return False

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return "DNA(sequence='{}')".format(self.sequence)

    def _check_validity(self):
        return all((nucleotide in 'GCAT' for nucleotide in self.sequence.upper()))

    @property
    def gc_content(self):
        return sum((nucleotide in 'GC' for nucleotide in self.sequence.upper())) / len(self.sequence)

    def gc_content(self):
        return sum((nucleotide in 'GC' for nucleotide in self.sequence.upper())) / len(self.sequence)

    @property
    def complimentary_sequence(self):
        return DNA(''.join((complimentary_nucleotides[nt.upper()] for nt in self.sequence)))

    @property
    def split_DNA_triplets(self):
        """
        This functions divides DNA sequence into triplets, irrespective of where the start codon is.
        """
        return [self.sequence[i:i + 3] for i in range(0, len(self.sequence), 3)]

    @property
    def find_first_start_site(self):
        """
        Seeks position of the first start codon, if present.
        """
        for i in range(0, len(self.sequence)):
            if self.sequence[i:i + 3] == 'ATG':
                return i

        raise TypeError('No start codon found')

    def compliment(self):
        return DNA(''.join((complimentary_nucleotides[nt] for nt in self.sequence.upper())))

    def find_start_codons(self):
        """ Finds the start codon of a coding DNA sequence"""
        indices = []
        index = -1
        while True:
            index = self.sequence.find('ATG', index + 1)
            if index == -1:
                return indices
            indices.append(index)

    def transcribe(self):
        """Transcribes a DNA sequence into a RNA sequence"""
        compliment = str(self.complimentary_sequence)
        reverse_compliment = ''.join((compliment[i] for i in range(len(compliment) - 1, -1, -1)))
        reverse_compliment_rna = reverse_compliment.replace('T', 'U')
        return reverse_compliment_rna

    def gc_content(self):
        return 0.5

    @property
    def gc_content(self):
        return sum((nucleotide in 'GC' for nucleotide in self.sequence.upper())) / len(self.sequence)

    @property
    def complimentary_sequence(self):
        return DNA(''.join((complimentary_nucleotides[nt.upper()] for nt in self.sequence)))