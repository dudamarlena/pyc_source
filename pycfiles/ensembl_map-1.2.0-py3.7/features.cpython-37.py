# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ensembl_map/features.py
# Compiled at: 2020-04-24 16:50:04
# Size of source mod 2**32: 7387 bytes
from types import SimpleNamespace

class CDS(SimpleNamespace):
    __doc__ = 'CDS coordinate object.\n\n    Attributes:\n        biotype (str): biotype of the transcript\n        contig (str): name of the contig the feature is mapped to\n        end (int): end position, relative to the CDS\n        sequence (str): CDS sequence from `start` to `end`, inclusive\n        start (int): start position, relative to the CDS\n        strand (str): orientation on the contig ("+" or "-")\n        transcript (`pyensembl.Transcript`)\n        transcript_id (str): Ensembl transcript ID\n        transcript_name (str): Ensembl transcript name\n    '

    @classmethod
    def load(cls, transcript, start, end):
        if start > end:
            start, end = end, start
        sequence = getattr(transcript, 'coding_sequence', None)
        if sequence:
            sequence = sequence[start - 1:end]
        return cls(biotype=(getattr(transcript, 'biotype', None)),
          contig=(getattr(transcript, 'contig', None)),
          end=end,
          sequence=sequence,
          start=start,
          strand=(getattr(transcript, 'strand', None)),
          transcript_id=(getattr(transcript, 'transcript_id', None)),
          transcript_name=(getattr(transcript, 'transcript_name', None)))

    def to_tuple(self):
        return (
         self.transcript_id, self.start, self.end)


class Exon(SimpleNamespace):
    __doc__ = 'Exon coordinate object.\n\n    Attributes:\n        biotype (str): biotype of the transcript the exon belongs to\n        contig (str): name of the contig the exon is mapped to\n        end (int): end position, relative to the contig\n        exon (`pyensembl.Exon`)\n        exon_id (str): Ensembl exon ID\n        index (int): position of the exon relative to all exons in the transcript\n        start (int): start position, relative to the contig\n        strand (str): orientation on the contig ("+" or "-")\n        transcript (`pyensembl.Transcript`)\n        transcript_id (str): Ensembl transcript ID\n        transcript_name (str): Ensembl transcript name\n    '

    @classmethod
    def load(cls, transcript, start, end):
        if start > end:
            start, end = end, start
        exon, index = cls.index_exon(transcript, start, end)
        return cls(biotype=(getattr(transcript, 'biotype', None)),
          contig=(getattr(transcript, 'contig', None)),
          end=end,
          exon_id=(getattr(exon, 'exon_id', None)),
          index=index,
          start=start,
          strand=(getattr(transcript, 'strand', None)),
          transcript_id=(getattr(transcript, 'transcript_id', None)),
          transcript_name=(getattr(transcript, 'transcript_name', None)))

    @staticmethod
    def index_exon(transcript, start, end):
        exons = [(i, n) for n, i in enumerate(transcript.exons, 1) if start == i.start if end == i.end]
        if len(exons) < 1:
            raise ValueError(f"Exon ({start}, {end}) not found in transcript {transcript.transcript_id}")
        else:
            if len(exons) > 1:
                raise ValueError(f"Multiple exons ({start}, {end}) found in transcript {transcript.transcript_id}")
            else:
                return exons[0]

    def to_tuple(self):
        return (
         self.exon_id, self.start, self.end)


class Gene(SimpleNamespace):
    __doc__ = 'Gene coordinate object.\n\n    Attributes:\n        biotype (str): biotype of the gene\n        contig (str): name of the contig the feature is mapped to\n        end (int): end position, relative to the contig\n        gene (`pyensembl.Gene`)\n        gene_id (str): Ensembl gene ID\n        gene_name (str): Ensembl gene name\n        start (int): start position, relative to the contig\n        strand (str): orientation on the contig ("+" or "-")\n    '

    @classmethod
    def load(cls, transcript, start, end):
        if start > end:
            start, end = end, start
        gene = transcript.gene
        return cls(biotype=(getattr(gene, 'biotype', None)),
          contig=(getattr(gene, 'contig', None)),
          end=end,
          gene_id=(getattr(gene, 'gene_id', None)),
          gene_name=(getattr(gene, 'gene_name', None)),
          start=start,
          strand=(getattr(gene, 'strand', None)))

    def to_tuple(self):
        return (
         self.gene_id, self.start, self.end)


class Protein(SimpleNamespace):
    __doc__ = 'Protein coordinate object.\n\n    Attributes:\n        biotype (str): biotype of the transcript that encodes the protein (should be \'protein_coding\')\n        contig (str): name of the contig the protein is mapped to\n        end (int): end position, relative to the protein\n        protein_id (str): Ensembl protein ID\n        start (int): start position, relative to the protein\n        strand (str): orientation on the contig ("+" or "-")\n        sequence (str): protein sequence from `start` to `end`, inclusive\n        transcript (`pyensembl.Transcript`)\n    '

    @classmethod
    def load(cls, transcript, start, end):
        if start > end:
            start, end = end, start
        sequence = getattr(transcript, 'protein_sequence', None)
        if sequence:
            sequence = sequence[start - 1:end]
        return cls(biotype=(getattr(transcript, 'biotype', None)),
          contig=(getattr(transcript, 'contig', None)),
          end=end,
          protein_id=(getattr(transcript, 'protein_id', None)),
          sequence=sequence,
          start=start,
          strand=(getattr(transcript, 'strand', None)))

    def to_tuple(self):
        return (
         self.protein_id, self.start, self.end)


class Transcript(CDS):
    __doc__ = 'Transcript coordinate object.\n\n    Attributes:\n        biotype (str): biotype of the transcript\n        contig (str): name of the contig the feature is mapped to\n        end (int): end position, relative to the transcript\n        sequence (str): transcript sequence from `start` to `end`, inclusive\n        start (int): start position, relative to the transcript\n        strand (str): orientation on the contig ("+" or "-")\n        transcript (`pyensembl.Transcript`)\n        transcript_id (str): Ensembl transcript ID\n        transcript_name (str): Ensembl transcript name\n    '

    @classmethod
    def load(cls, transcript, start, end):
        if start > end:
            start, end = end, start
        sequence = getattr(transcript, 'sequence', None)
        if sequence:
            sequence = sequence[start - 1:end]
        return cls(biotype=(getattr(transcript, 'biotype', None)),
          contig=(getattr(transcript, 'contig', None)),
          end=end,
          sequence=sequence,
          start=start,
          strand=(getattr(transcript, 'strand', None)),
          transcript_id=(getattr(transcript, 'transcript_id', None)),
          transcript_name=(getattr(transcript, 'transcript_name', None)))


def get_load_function(to_type):
    if to_type == 'cds':
        return CDS.load
    if to_type == 'exon':
        return Exon.load
    if to_type == 'gene':
        return Gene.load
    if to_type == 'protein':
        return Protein.load
    if to_type == 'transcript':
        return Transcript.load
    raise TypeError(f"Could not get parse function for {to_type}")