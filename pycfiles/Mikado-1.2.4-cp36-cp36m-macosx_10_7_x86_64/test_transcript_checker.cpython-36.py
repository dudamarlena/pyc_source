# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/venturil/workspace/mikado/Mikado/tests/test_transcript_checker.py
# Compiled at: 2018-05-23 17:14:36
# Size of source mod 2**32: 16847 bytes
import gzip, os, tempfile, unittest, pkg_resources, pyfaidx
from Mikado.transcripts.transcriptchecker import TranscriptChecker
from Mikado.parsers.GFF import GffLine
from Mikado.parsers.GTF import GtfLine
from Mikado.transcripts.transcript import Transcript

class TChekerTester(unittest.TestCase):
    temp_genome = None

    @classmethod
    def setUpClass(cls):
        cls.temp_genome = tempfile.NamedTemporaryFile(mode='wb', suffix='.fa')
        with pkg_resources.resource_stream('Mikado.tests', 'chr5.fas.gz') as (comp):
            cls.temp_genome.write(gzip.decompress(comp.read()))
        cls.temp_genome.flush()
        cls.fasta = pyfaidx.Fasta(cls.temp_genome.name)

    def setUp(self):
        self.model_lines = 'Chr5\ttair10\ttranscript\t26584797\t26595528\t100\t+\t.\tID=c58_g1_i3.mrna1.19;Parent=c58_g1_i3.path1.19;Name=c58_g1_i3.mrna1.19;gene_name=c58_g1_i3\n    Chr5\ttair10\texon\t26584797\t26584879\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon1;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26585220\t26585273\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon2;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26585345\t26585889\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon3;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26585982\t26586294\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon4;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26586420\t26586524\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon5;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26586638\t26586850\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon6;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26586934\t26586996\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon7;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26587084\t26587202\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon8;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26587287\t26587345\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon9;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26587427\t26587472\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon10;Parent=c58_g1_i3.mrna1.19\n    Chr5\ttair10\texon\t26595411\t26595528\t.\t+\t.\tID=c58_g1_i3.mrna1.19.exon11;Parent=c58_g1_i3.mrna1.19'
        self.gff_lines = []
        for line in self.model_lines.split('\n'):
            line = line.rstrip().lstrip()
            line = GffLine(line)
            self.gff_lines.append(line)

        self.model = Transcript(self.gff_lines[0])
        self.model.add_exons(self.gff_lines[1:])
        self.model.finalize()
        self.exons = [self.fasta[line.chrom][line.start - 1:line.end] for line in self.gff_lines[1:]]
        self.assertEqual(sum([len(exon) for exon in self.exons]), 1718, self.exons)
        self.model_fasta = self.fasta['Chr5'][self.model.start - 1:self.model.end]
        self.assertEqual(self.gff_lines[1].start, 26584797)
        self.assertEqual(self.gff_lines[1].end, 26584879)
        self.assertEqual(self.model.exons[0][0], self.gff_lines[1].start)
        self.assertEqual(self.model.exons[0][1], self.gff_lines[1].end)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls.temp_genome, 'close'):
            cls.temp_genome.close()
            cls.fasta.close()
            os.remove('{}.fai'.format(cls.temp_genome.name))

    def test_translation_table(self):
        self.assertEqual(TranscriptChecker.get_translation_table(), {65:84, 
         67:71,  71:67,  84:65})

    def test_rev_complement(self):
        string = 'AGTCGTGCAGNGTCGAAGTGCAACAGTGC'
        self.assertEqual(TranscriptChecker.rev_complement(string), 'GCACTGTTGCACTTCGACNCTGCACGACT')

    def test_init(self):
        tcheck = TranscriptChecker(self.model, self.model_fasta)
        self.assertEqual(tcheck.cdna_length, 1718)
        self.assertEqual(sorted(tcheck.exons), sorted([(exon.start, exon.end) for exon in self.exons]))
        self.assertEqual(tcheck.fasta_seq, self.model_fasta)

    def test_check_reverse_strand(self):
        self.model.strand = '-'
        tcheck = TranscriptChecker((self.model), (self.model_fasta), strand_specific=False)
        tcheck.check_strand()
        self.assertEqual(tcheck.strand, '+')

    def test_check_strand_not_reversed(self):
        self.model.strand = '-'
        tcheck = TranscriptChecker((self.model), (self.model_fasta), strand_specific=True)
        tcheck.check_strand()
        self.assertEqual(tcheck.strand, '+')
        self.assertFalse(tcheck.attributes.get('canonical_on_reverse_strand', False))
        self.assertFalse(tcheck.suspicious_splicing)

    def test_monoexonic(self):
        exon = self.gff_lines[1]
        transcript_line = self.gff_lines[0]
        transcript_line.end = exon.end
        model = Transcript(transcript_line)
        model.add_exon(exon)
        model.finalize()
        fasta = self.fasta[model.chrom][model.start - 1:model.end]
        tcheck = TranscriptChecker((model.copy()), fasta, strand_specific=False)
        tcheck.check_strand()
        self.assertIsNone(tcheck.strand)
        tcheck = TranscriptChecker((model.copy()), fasta, strand_specific=True)
        tcheck.check_strand()
        self.assertEqual(tcheck.strand, '+')
        neg = model.copy()
        neg.strand = '-'
        tcheck = TranscriptChecker((neg.copy()), fasta, strand_specific=False)
        tcheck.check_strand()
        self.assertIsNone(tcheck.strand)
        tcheck = TranscriptChecker((neg.copy()), fasta, strand_specific=True)
        tcheck.check_strand()
        self.assertEqual(tcheck.strand, '-')

    def test_negative(self):
        gtf_lines = 'Chr5\tCufflinks\ttranscript\t26575364\t26578163\t1000\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";exon_number "1";FPKM "2.9700103727";conf_hi "3.260618";frac "0.732092";cov "81.895309";conf_lo "2.679403";\nChr5\tCufflinks\texon\t26575364\t26575410\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26575495\t26575620\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26575711\t26575797\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26575885\t26575944\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26576035\t26576134\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26576261\t26577069\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26577163\t26577288\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26577378\t26577449\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";\nChr5\tCufflinks\texon\t26577856\t26578163\t.\t-\t.\tgene_id "cufflinks_star_at.23553";transcript_id "cufflinks_star_at.23553.1";'
        gtf_lines = [GtfLine(line) for line in gtf_lines.split('\n')]
        self.assertEqual(len([_ for _ in gtf_lines if _.header]), 0)
        transcript = Transcript(gtf_lines[0])
        transcript.add_exons(gtf_lines[1:])
        transcript.finalize()
        fasta_seq = self.fasta[transcript.chrom][transcript.start - 1:transcript.end]
        tr_neg = transcript.copy()
        tchecker = TranscriptChecker(tr_neg, fasta_seq, strand_specific=False)
        self.assertEqual(tchecker.strand, '-')
        self.assertEqual(tchecker.fasta_seq, fasta_seq)
        tchecker.check_strand()
        self.assertEqual(tchecker.strand, '-')
        tr_neg = transcript.copy()
        tr_neg.strand = '+'
        for ss in (False, True):
            with self.subTest(ss=ss):
                tchecker = TranscriptChecker((tr_neg.copy()), fasta_seq, strand_specific=ss)
                tchecker.check_strand()
                self.assertEqual(tchecker.strand, '-')

    def test_suspicious(self):
        self.model.attributes['mixed_splices'] = '6positive,1negative'
        self.assertTrue(self.model.suspicious_splicing)
        del self.model.attributes['mixed_splices']
        self.assertFalse(self.model.suspicious_splicing)
        self.model.attributes['canonical_number'] = 0
        self.assertFalse(self.model.suspicious_splicing)
        del self.model.attributes['canonical_number']
        self.model.attributes['canonical_on_reverse_strand'] = True
        self.assertTrue(self.model.suspicious_splicing)
        self.model.attributes['canonical_on_reverse_strand'] = False
        self.assertFalse(self.model.suspicious_splicing)
        self.model.attributes['mixed_splices'] = '6positive,1negative'
        self.assertTrue(self.model.suspicious_splicing)
        del self.model.attributes['mixed_splices']
        del self.model.attributes['canonical_on_reverse_strand']
        self.model.attributes['canonical_number'] = 0
        self.assertFalse(self.model.suspicious_splicing)
        self.assertTrue(self.model.only_non_canonical_splicing)
        self.model.attributes['canonical_on_reverse_strand'] = True
        self.assertTrue(self.model.suspicious_splicing)
        self.assertTrue(self.model.only_non_canonical_splicing)
        del self.model.attributes['canonical_on_reverse_strand']
        self.model.attributes['mixed_splices'] = '6positive,1negative'
        self.assertTrue(self.model.suspicious_splicing)
        self.assertTrue(self.model.only_non_canonical_splicing)

    def test_monoexonic_suspicious(self):
        """A monoexonic transcript should never appear as a suspicious transcript, in terms of splicing."""
        exon = self.gff_lines[1]
        transcript_line = self.gff_lines[0]
        transcript_line.end = exon.end
        model = Transcript(transcript_line)
        model.add_exon(exon)
        model.finalize()
        model.attributes['mixed_splices'] = '6positive,1negative'
        self.assertFalse(model.suspicious_splicing)
        del model.attributes['mixed_splices']
        self.assertFalse(model.suspicious_splicing)
        model.attributes['canonical_number'] = 0
        self.assertFalse(model.suspicious_splicing)
        del model.attributes['canonical_number']
        model.attributes['canonical_on_reverse_strand'] = True
        self.assertFalse(model.suspicious_splicing)
        model.attributes['canonical_on_reverse_strand'] = False
        self.assertFalse(model.suspicious_splicing)
        model.attributes['mixed_splices'] = '6positive,1negative'
        self.assertFalse(model.suspicious_splicing)
        del model.attributes['mixed_splices']
        del model.attributes['canonical_on_reverse_strand']
        model.attributes['canonical_number'] = 0
        self.assertFalse(model.suspicious_splicing)
        self.assertFalse(model.only_non_canonical_splicing)
        model.attributes['canonical_on_reverse_strand'] = True
        self.assertFalse(model.suspicious_splicing)
        self.assertFalse(model.only_non_canonical_splicing)
        del model.attributes['canonical_on_reverse_strand']
        model.attributes['mixed_splices'] = '6positive,1negative'
        self.assertFalse(model.suspicious_splicing)
        self.assertFalse(model.only_non_canonical_splicing)


class StopCodonChecker(unittest.TestCase):

    def test_positive_strand(self):
        gtf_lines = 'chr1A\tSelf_CESAR/windows_chr1A.gp\ttranscript\t265021906\t265026255\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265021906\t265021971\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tCDS\t265021906\t265021971\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265022056\t265026255\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tCDS\t265022056\t265026252\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstart_codon\t265021906\t265021908\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstop_codon\t265026253\t265026255\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";'
        gtf_lines = [GtfLine(_) for _ in gtf_lines.split('\n')]
        t = Transcript(gtf_lines[0])
        t.add_exons(gtf_lines[1:])
        t.finalize()
        self.assertEqual(t.start, t.combined_cds_start)
        self.assertEqual(t.end, t.combined_cds_end)

    def test_positive_strand_split(self):
        gtf_lines = 'chr1A\tSelf_CESAR/windows_chr1A.gp\ttranscript\t265021906\t265026355\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265021906\t265021971\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tCDS\t265021906\t265021971\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265022056\t265026253\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tCDS\t265022056\t265026252\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265026354\t265026355\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstart_codon\t265021906\t265021908\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstop_codon\t265026253\t265026253\t.\t+\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstop_codon\t265026354\t265026355\t.\t+\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";'
        gtf_lines = [GtfLine(_) for _ in gtf_lines.split('\n')]
        t = Transcript(gtf_lines[0])
        t.add_exons(gtf_lines[1:])
        t.finalize()
        self.assertEqual(t.start, t.combined_cds_start)
        self.assertEqual(t.end, t.combined_cds_end)

    def test_negative_strand(self):
        gtf_lines = 'chr1A\tSelf_CESAR/windows_chr1A.gp\ttranscript\t265021806\t265026255\t.\t-\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265021806\t265021807\t.\t-\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265021908\t265021971\t.\t-\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tCDS\t265021909\t265021971\t.\t-\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\texon\t265022056\t265026255\t.\t-\t.\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tCDS\t265022056\t265026255\t.\t-\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstop_codon\t265021806\t265021807\t.\t-\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstop_codon\t265021908\t265021908\t.\t-\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "1"; exon_id "TraesCS1A01G152900.1.1";\nchr1A\tSelf_CESAR/windows_chr1A.gp\tstart_codon\t265026253\t265026255\t.\t-\t0\tgene_id "TraesCS1A01G152900.1"; transcript_id "TraesCS1A01G152900.1"; exon_number "2"; exon_id "TraesCS1A01G152900.1.2";'
        gtf_lines = [GtfLine(_) for _ in gtf_lines.split('\n')]
        t = Transcript(gtf_lines[0])
        t.add_exons(gtf_lines[1:])
        t.finalize()
        self.assertEqual(t.start, t.combined_cds_end)
        self.assertEqual(t.end, t.combined_cds_start)


if __name__ == '__main__':
    unittest.main()