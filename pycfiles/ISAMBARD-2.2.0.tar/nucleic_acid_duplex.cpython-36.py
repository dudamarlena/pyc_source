# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/isambard/src/isambard/specifications/nucleic_acid_duplex.py
# Compiled at: 2018-04-18 05:10:39
# Size of source mod 2**32: 2851 bytes
"""Contains code for generating nucleic acid duplexes."""
from ampal import Assembly
from ampal.geometry import dihedral
from .nucleic_acid_strand import NucleicAcidStrand

def generate_antisense_sequence(sequence):
    """Creates the antisense sequence of a DNA strand."""
    dna_antisense = {'A':'T', 
     'T':'A', 
     'C':'G', 
     'G':'C'}
    antisense = [dna_antisense[x] for x in sequence[::-1]]
    return ''.join(antisense)


class DNADuplex(Assembly):
    __doc__ = 'Creates a DNA duplex from a single strand of helical DNA.\n\n    Parameters\n    ----------\n    strand: NucleicAcidStrand\n        DNA single strand helix.\n    '

    def __init__(self, strand):
        super().__init__([strand, self.generate_complementary_strand(strand)])
        self.relabel_polymers()

    @classmethod
    def from_sequence(cls, sequence, phos_3_prime=False):
        """Creates a DNA duplex from a nucleotide sequence.

        Parameters
        ----------
        sequence: str
            Nucleotide sequence.
        phos_3_prime: bool, optional
            If false the 5' and the 3' phosphor will be omitted.
        """
        strand1 = NucleicAcidStrand(sequence, phos_3_prime=phos_3_prime)
        duplex = cls(strand1)
        return duplex

    @classmethod
    def from_start_and_end(cls, start, end, sequence, phos_3_prime=False):
        """Creates a DNA duplex from a start and end point.

            Parameters
            ----------
            start: [float, float, float]
                Start of the build axis.
            end: [float, float, float]
                End of build axis.
            sequence: str
                Nucleotide sequence.
            phos_3_prime: bool, optional
                If false the 5' and the 3' phosphor will be omitted."""
        strand1 = NucleicAcidStrand.from_start_and_end(start,
          end, sequence, phos_3_prime=phos_3_prime)
        duplex = cls(strand1)
        return duplex

    @staticmethod
    def generate_complementary_strand(strand1):
        """Takes a SingleStrandHelix and creates the antisense strand."""
        rise_adjust = strand1.rise_per_nucleotide * strand1.axis.unit_tangent * 2
        strand2 = NucleicAcidStrand.from_start_and_end((strand1.helix_end - rise_adjust),
          (strand1.helix_start - rise_adjust), (generate_antisense_sequence(strand1.base_sequence)),
          phos_3_prime=(strand1.phos_3_prime))
        ad_ang = dihedral(strand1[0]["C1'"]._vector, strand1.axis.start, strand2.axis.start + rise_adjust, strand2[(-1)]["C1'"]._vector)
        strand2.rotate((225.0 + ad_ang),
          (strand2.axis.unit_tangent), point=(strand2.helix_start))
        return strand2


__author__ = 'Christopher W. Wood'