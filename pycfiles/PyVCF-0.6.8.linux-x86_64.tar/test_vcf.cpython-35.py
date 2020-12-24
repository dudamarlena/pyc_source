# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/vcf/test/test_vcf.py
# Compiled at: 2016-03-18 12:18:33
# Size of source mod 2**32: 55069 bytes
import unittest
try:
    unittest.skip
except AttributeError:
    import unittest2 as unittest

import doctest, os, subprocess, pickle
from io import StringIO
import subprocess, sys
try:
    import pysam
except ImportError:
    pysam = None

import vcf
from vcf import model, utils
IS_PYTHON2 = sys.version_info[0] == 2
IS_NOT_PYPY = 'PyPy' not in sys.version
suite = doctest.DocTestSuite(vcf)

def fh(fname, mode='rt'):
    return open(os.path.join(os.path.dirname(__file__), fname), mode)


class TestVcfSpecs(unittest.TestCase):

    def test_vcf_4_0(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        self.assertEqual(reader.metadata['fileformat'], 'VCFv4.0')
        for r in reader:
            if r.POS == 1230237:
                if not r.is_monomorphic:
                    raise AssertionError
            elif not not r.is_monomorphic:
                raise AssertionError
            if 'AF' in r.INFO:
                self.assertEqual(type(r.INFO['AF']), type([]))
            for c in r:
                assert c
                if c.called:
                    self.assertEqual(type(c.data.GQ), type(1))
                    if 'HQ' in c.data and c.data.HQ is not None:
                        self.assertEqual(type(c.data.HQ), type([]))

    def test_vcf_4_1(self):
        reader = vcf.Reader(fh('example-4.1.vcf'))
        self.assertEqual(reader.metadata['fileformat'], 'VCFv4.1')
        self.assertEqual(reader.contigs['20'].length, 62435964)
        for r in reader:
            for c in r:
                if not c:
                    raise AssertionError

    def test_vcf_4_1_sv(self):
        reader = vcf.Reader(fh('example-4.1-sv.vcf'))
        assert 'SVLEN' in reader.infos
        assert 'fileDate' in reader.metadata
        assert 'DEL' in reader.alts
        for r in reader:
            print(r)
            for a in r.ALT:
                print(a)

            for c in r:
                print(c)
                if not c:
                    raise AssertionError

    def test_vcf_4_1_bnd(self):
        reader = vcf.Reader(fh('example-4.1-bnd.vcf'))
        for r in reader:
            print(r)
            for a in r.ALT:
                print(a)

            if r.ID == 'bnd1':
                self.assertEqual(len(r.ALT), 1)
                self.assertEqual(r.ALT[0].type, 'BND')
                self.assertEqual(r.ALT[0].chr, '2')
                self.assertEqual(r.ALT[0].pos, 3)
                self.assertEqual(r.ALT[0].orientation, False)
                self.assertEqual(r.ALT[0].remoteOrientation, True)
                self.assertEqual(r.ALT[0].connectingSequence, 'T')
            if r.ID == 'bnd4':
                self.assertEqual(len(r.ALT), 1)
                self.assertEqual(r.ALT[0].type, 'BND')
                self.assertEqual(r.ALT[0].chr, '1')
                self.assertEqual(r.ALT[0].pos, 2)
                self.assertEqual(r.ALT[0].orientation, True)
                self.assertEqual(r.ALT[0].remoteOrientation, False)
                self.assertEqual(r.ALT[0].connectingSequence, 'G')
            for c in r:
                print(c)
                if not c:
                    raise AssertionError

    def test_vcf_4_2(self):
        reader = vcf.Reader(fh('example-4.2.vcf'))
        self.assertEqual(reader.metadata['fileformat'], 'VCFv4.2')
        self.assertEqual(reader.infos['DP'].source, None)
        self.assertEqual(reader.infos['DP'].version, None)
        self.assertEqual(reader.infos['VDB'].source, None)
        self.assertEqual(reader.infos['VDB'].version, '3')
        for r in reader:
            for c in r:
                if not c:
                    raise AssertionError

    def test_contig_idonly(self):
        """Test VCF inputs with ##contig inputs containing only IDs. produced by bcftools 1.2+
        """
        reader = vcf.Reader(fh('contig_idonly.vcf'))
        for cid, contig in list(reader.contigs.items()):
            if cid == '1':
                if not contig.length is None:
                    raise AssertionError
            else:
                if cid == '2':
                    if not contig.length == 2000:
                        raise AssertionError
                elif cid == '3':
                    if not contig.length == 3000:
                        raise AssertionError


class TestGatkOutput(unittest.TestCase):
    filename = 'gatk.vcf'
    samples = [
     'BLANK', 'NA12878', 'NA12891', 'NA12892',
     'NA19238', 'NA19239', 'NA19240']
    formats = ['AD', 'DP', 'GQ', 'GT', 'PL']
    infos = ['AC', 'AF', 'AN', 'BaseQRankSum', 'DB', 'DP', 'DS',
     'Dels', 'FS', 'HRun', 'HaplotypeScore', 'InbreedingCoeff',
     'MQ', 'MQ0', 'MQRankSum', 'QD', 'ReadPosRankSum']
    n_calls = 37

    def setUp(self):
        self.reader = vcf.Reader(fh(self.filename))

    def testSamples(self):
        self.assertEqual(self.reader.samples, self.samples)

    def testFormats(self):
        self.assertEqual(set(self.reader.formats), set(self.formats))

    def testInfos(self):
        self.assertEqual(set(self.reader.infos), set(self.infos))

    def testCalls(self):
        n = 0
        for site in self.reader:
            n += 1
            self.assertEqual(len(site.samples), len(self.samples))
            for s in self.samples:
                if not site.genotype(s):
                    raise AssertionError

            self.assertEqual([x.sample for x in site.samples], self.samples)

        self.assertEqual(n, self.n_calls)


class TestFreebayesOutput(TestGatkOutput):
    filename = 'freebayes.vcf'
    formats = ['AO', 'DP', 'GL', 'GLE', 'GQ', 'GT', 'QA', 'QR', 'RO']
    infos = ['AB', 'ABP', 'AC', 'AF', 'AN', 'AO', 'BVAR', 'CIGAR',
     'DB', 'DP', 'DPRA', 'EPP', 'EPPR', 'HWE', 'LEN', 'MEANALT',
     'NUMALT', 'RPP', 'MQMR', 'ODDS', 'MQM', 'PAIREDR', 'PAIRED',
     'SAP', 'XRM', 'RO', 'REPEAT', 'XRI', 'XAS', 'XAI', 'SRP',
     'XAM', 'XRS', 'RPPR', 'NS', 'RUN', 'CpG', 'TYPE']
    n_calls = 104

    def testParse(self):
        reader = vcf.Reader(fh('freebayes.vcf'))
        print(reader.samples)
        self.assertEqual(len(reader.samples), 7)
        n = 0
        for r in reader:
            n += 1
            for x in r:
                if not x:
                    raise AssertionError

        self.assertEqual(n, self.n_calls)


class TestSamtoolsOutput(unittest.TestCase):

    def testParse(self):
        reader = vcf.Reader(fh('samtools.vcf'))
        self.assertEqual(len(reader.samples), 1)
        self.assertEqual(sum(1 for _ in reader), 11)


class TestBcfToolsOutput(unittest.TestCase):

    def testParse(self):
        reader = vcf.Reader(fh('bcftools.vcf'))
        self.assertEqual(len(reader.samples), 1)
        for r in reader:
            for s in r.samples:
                s.phased


class TestIssue214(unittest.TestCase):
    __doc__ = ' See https://github.com/jamescasbon/PyVCF/issues/214 '

    def test_issue_214_is_snp(self):
        reader = vcf.Reader(fh('issue-214.vcf'))
        r = next(reader)
        self.assertTrue(r.is_snp)

    def test_issue_214_var_type(self):
        reader = vcf.Reader(fh('issue-214.vcf'))
        r = next(reader)
        self.assertEqual(r.var_type, 'snp')

    def test_issue_214_ref_is_del_is_snp(self):
        reader = vcf.Reader(fh('issue-214.vcf'))
        next(reader)
        r = next(reader)
        self.assertTrue(r.is_snp)

    def test_issue_214_ref_is_del_var_type(self):
        reader = vcf.Reader(fh('issue-214.vcf'))
        next(reader)
        r = next(reader)
        self.assertEqual(r.var_type, 'snp')


class Test1kg(unittest.TestCase):

    def testParse(self):
        reader = vcf.Reader(fh('1kg.vcf.gz', 'rb'))
        assert 'FORMAT' in reader._column_headers
        self.assertEqual(len(reader.samples), 629)
        for _ in reader:
            pass

    def test_issue_49(self):
        """docstring for test_issue_49"""
        reader = vcf.Reader(fh('issue_49.vcf', 'r'))
        self.assertEqual(len(reader.samples), 0)
        for _ in reader:
            pass


class Test1kgSites(unittest.TestCase):

    def test_reader(self):
        """The samples attribute should be the empty list."""
        reader = vcf.Reader(fh('1kg.sites.vcf', 'r'))
        assert 'FORMAT' not in reader._column_headers
        self.assertEqual(reader.samples, [])
        for record in reader:
            self.assertEqual(record.samples, [])

    def test_writer(self):
        """FORMAT should not be written if not present in the template and no
        extra tab character should be printed if there are no FORMAT fields."""
        reader = vcf.Reader(fh('1kg.sites.vcf', 'r'))
        out = StringIO()
        writer = vcf.Writer(out, reader, lineterminator='\n')
        for record in reader:
            writer.write_record(record)

        out.seek(0)
        out_str = out.getvalue()
        for line in out_str.split('\n'):
            if line.startswith('##'):
                pass
            elif line.startswith('#CHROM'):
                assert 'FORMAT' not in line
                if not not line.endswith('\t'):
                    raise AssertionError


class TestGoNL(unittest.TestCase):

    def testParse(self):
        reader = vcf.Reader(fh('gonl.chr20.release4.gtc.vcf'))
        for _ in reader:
            pass

    def test_contig_line(self):
        reader = vcf.Reader(fh('gonl.chr20.release4.gtc.vcf'))
        self.assertEqual(reader.contigs['1'].length, 249250621)


class TestStringAsFlag(unittest.TestCase):

    def test_string_as_flag(self):
        """A flag INFO field is declared as string (not allowed by the spec,
        but seen in practice)."""
        reader = vcf.Reader(fh('string_as_flag.vcf', 'r'))
        for _ in reader:
            pass


class TestInfoOrder(unittest.TestCase):

    def _assert_order(self, definitions, fields):
        """
        Elements common to both lists should be in the same order. Elements
        only in `fields` should be last and in alphabetical order.
        """
        used_definitions = [d for d in definitions if d in fields]
        self.assertEqual(used_definitions, fields[:len(used_definitions)])
        self.assertEqual(fields[len(used_definitions):], sorted(fields[len(used_definitions):]))

    def test_writer(self):
        """
        Order of INFO fields should be compatible with the order of their
        definition in the header and undefined fields should be last and in
        alphabetical order.
        """
        reader = vcf.Reader(fh('1kg.sites.vcf', 'r'))
        out = StringIO()
        writer = vcf.Writer(out, reader, lineterminator='\n')
        for record in reader:
            writer.write_record(record)

        out.seek(0)
        out_str = out.getvalue()
        definitions = []
        for line in out_str.split('\n'):
            if line.startswith('##INFO='):
                definitions.append(line.split('ID=')[1].split(',')[0])
            if not not line:
                if line.startswith('#'):
                    pass
                else:
                    fields = [f.split('=')[0] for f in line.split('\t')[7].split(';')]
                    self._assert_order(definitions, fields)


class TestInfoTypeCharacter(unittest.TestCase):

    def test_parse(self):
        reader = vcf.Reader(fh('info-type-character.vcf'))
        record = next(reader)
        self.assertEqual(record.INFO['FLOAT_1'], 123.456)
        self.assertEqual(record.INFO['CHAR_1'], 'Y')
        self.assertEqual(record.INFO['FLOAT_N'], [123.456])
        self.assertEqual(record.INFO['CHAR_N'], ['Y'])

    def test_write(self):
        reader = vcf.Reader(fh('info-type-character.vcf'))
        out = StringIO()
        writer = vcf.Writer(out, reader)
        records = list(reader)
        for record in records:
            writer.write_record(record)

        out.seek(0)
        reader2 = vcf.Reader(out)
        for l, r in zip(records, reader2):
            self.assertEqual(l.INFO, r.INFO)


class TestParseMetaLine(unittest.TestCase):

    def test_parse(self):
        reader = vcf.Reader(fh('parse-meta-line.vcf'))
        f = reader.metadata['MYFIELD'][0]
        self.assertEqual(f['ID'], 'SomeField')
        self.assertEqual(f['Version'], '3.4-0-g7e26428')
        self.assertEqual(f['Date'], '"Wed Oct 07 09:11:47 CEST 2015"')
        self.assertEqual(f['Options'], '"< 4 and > 3"')
        next(reader)

    def test_write(self):
        reader = vcf.Reader(fh('parse-meta-line.vcf'))
        out = StringIO()
        writer = vcf.Writer(out, reader)
        records = list(reader)
        for record in records:
            writer.write_record(record)

        out.seek(0)
        reader2 = vcf.Reader(out)
        f = reader2.metadata['MYFIELD'][0]
        self.assertEqual(f['ID'], 'SomeField')
        self.assertEqual(f['Version'], '3.4-0-g7e26428')
        self.assertEqual(f['Date'], '"Wed Oct 07 09:11:47 CEST 2015"')
        self.assertEqual(f['Options'], '"< 4 and > 3"')
        for l, r in zip(records, reader2):
            self.assertEqual(l.INFO, r.INFO)


class TestGatkOutputWriter(unittest.TestCase):

    def testWrite(self):
        reader = vcf.Reader(fh('gatk.vcf'))
        out = StringIO()
        writer = vcf.Writer(out, reader)
        records = list(reader)
        for record in records:
            writer.write_record(record)

        out.seek(0)
        out_str = out.getvalue()
        for line in out_str.split('\n'):
            if line.startswith('##contig'):
                if not line.startswith('##contig=<'):
                    raise AssertionError('Found dictionary in contig line: {0}'.format(line))

        print(out_str)
        reader2 = vcf.Reader(out)
        self.assertEqual(reader.samples, reader2.samples)
        self.assertEqual(reader.formats, reader2.formats)
        self.assertEqual(reader.infos, reader2.infos)
        self.assertEqual(reader.contigs, reader2.contigs)
        for l, r in zip(records, reader2):
            self.assertEqual(l.samples, r.samples)
            for l_call, r_call in zip(l.samples, r.samples):
                self.assertEqual(l_call.data, r_call.data)


class TestBcfToolsOutputWriter(unittest.TestCase):

    def testWrite(self):
        reader = vcf.Reader(fh('bcftools.vcf'))
        out = StringIO()
        writer = vcf.Writer(out, reader)
        records = list(reader)
        for record in records:
            writer.write_record(record)

        out.seek(0)
        print(out.getvalue())
        reader2 = vcf.Reader(out)
        self.assertEqual(reader.samples, reader2.samples)
        self.assertEqual(reader.formats, reader2.formats)
        self.assertEqual(reader.infos, reader2.infos)
        for l, r in zip(records, reader2):
            self.assertEqual(l.samples, r.samples)
            for l_call, r_call in zip(l.samples, r.samples):
                self.assertEqual(l_call.data, r_call.data)


class TestWriterDictionaryMeta(unittest.TestCase):

    def testWrite(self):
        reader = vcf.Reader(fh('example-4.1-bnd.vcf'))
        out = StringIO()
        writer = vcf.Writer(out, reader)
        records = list(reader)
        for record in records:
            writer.write_record(record)

        out.seek(0)
        out_str = out.getvalue()
        for line in out_str.split('\n'):
            if line.startswith('##PEDIGREE'):
                self.assertEqual(line, '##PEDIGREE=<Derived="Tumor",Original="Germline">')
            if line.startswith('##SAMPLE'):
                if not line.startswith('##SAMPLE=<'):
                    raise AssertionError('Found dictionary in meta line: {0}'.format(line))


class TestSamplesSpace(unittest.TestCase):
    filename = 'samples-space.vcf'
    samples = ['NA 00001', 'NA 00002', 'NA 00003']

    def test_samples(self):
        self.reader = vcf.Reader(fh(self.filename), strict_whitespace=True)
        self.assertEqual(self.reader.samples, self.samples)


class TestMetadataWhitespace(unittest.TestCase):
    filename = 'metadata-whitespace.vcf'

    def test_metadata_whitespace(self):
        """
        Test parsing metadata header lines with whitespace.
        """
        self.reader = vcf.Reader(fh(self.filename))
        info_indel = self.reader.infos['INDEL']
        assert info_indel.id == 'INDEL'
        assert info_indel.num == 0
        assert info_indel.type == 'Flag'
        assert info_indel.desc == 'Indicates that the variant is an INDEL.'
        for r in self.reader:
            for c in r:
                pass


class TestMixedFiltering(unittest.TestCase):
    filename = 'mixed-filtering.vcf'

    def test_mixed_filtering(self):
        """
        Test mix of FILTER values (pass, filtered, no filtering).
        """
        reader = vcf.Reader(fh(self.filename))
        self.assertEqual(next(reader).FILTER, [])
        self.assertEqual(next(reader).FILTER, ['q10'])
        self.assertEqual(next(reader).FILTER, [])
        self.assertEqual(next(reader).FILTER, None)
        self.assertEqual(next(reader).FILTER, ['q10', 'q50'])


class TestRecord(unittest.TestCase):

    def test_num_calls(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            num_calls = var.num_hom_ref + var.num_hom_alt + var.num_het + var.num_unknown
            self.assertEqual(len(var.samples), num_calls)

    def test_dunder_eq(self):
        rec = next(vcf.Reader(fh('example-4.0.vcf')))
        self.assertFalse(rec == None)
        self.assertFalse(None == rec)

    def test_call_rate(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            call_rate = var.call_rate
            if var.POS == 14370:
                self.assertEqual(1.0, call_rate)
            if var.POS == 17330:
                self.assertEqual(1.0, call_rate)
            if var.POS == 1110696:
                self.assertEqual(1.0, call_rate)
            if var.POS == 1230237:
                self.assertEqual(1.0, call_rate)
            elif var.POS == 1234567:
                self.assertEqual(0.6666666666666666, call_rate)

    def test_aaf(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            aaf = var.aaf
            if var.POS == 14370:
                self.assertEqual([0.5], aaf)
            if var.POS == 17330:
                self.assertEqual([0.16666666666666666], aaf)
            if var.POS == 1110696:
                self.assertEqual([0.3333333333333333, 0.6666666666666666], aaf)
            if var.POS == 1230237:
                self.assertEqual([0.0], aaf)
            elif var.POS == 1234567:
                self.assertEqual([0.5, 0.25], aaf)

        reader = vcf.Reader(fh('example-4.1-ploidy.vcf'))
        for var in reader:
            aaf = var.aaf
            if var.POS == 60034:
                self.assertEqual([0.6666666666666666], aaf)
            elif var.POS == 60387:
                self.assertEqual([0.3333333333333333], aaf)

    def test_pi(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            pi = var.nucl_diversity
            if var.POS == 14370:
                self.assertEqual(0.6, pi)
            if var.POS == 17330:
                self.assertEqual(0.3333333333333333, pi)
            if var.POS == 1110696:
                self.assertEqual(None, pi)
            if var.POS == 1230237:
                self.assertEqual(0.0, pi)
            elif var.POS == 1234567:
                self.assertEqual(None, pi)

    def test_heterozygosity(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            het = var.heterozygosity
            if var.POS == 14370:
                self.assertEqual(0.5, het)
            if var.POS == 17330:
                self.assertEqual(0.2777777777777777, het)
            if var.POS == 1110696:
                self.assertEqual(0.4444444444444444, het)
            if var.POS == 1230237:
                self.assertEqual(0.0, het)
            elif var.POS == 1234567:
                self.assertEqual(0.625, het)

    def test_is_snp(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for r in reader:
            print(r)
            for c in r:
                print(c)
                if not c:
                    raise AssertionError

        for var in reader:
            is_snp = var.is_snp
            if var.POS == 14370:
                self.assertEqual(True, is_snp)
            if var.POS == 17330:
                self.assertEqual(True, is_snp)
            if var.POS == 1110696:
                self.assertEqual(True, is_snp)
            if var.POS == 1230237:
                self.assertEqual(False, is_snp)
            elif var.POS == 1234567:
                self.assertEqual(False, is_snp)

    def test_is_snp_for_n_alt(self):
        record = model._Record('1', 10, 'id1', 'C', [
         model._Substitution('N')], None, None, {}, None, {}, None)
        self.assertTrue(record.is_snp)

    def test_is_indel(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            is_indel = var.is_indel
            if var.POS == 14370:
                self.assertEqual(False, is_indel)
            if var.POS == 17330:
                self.assertEqual(False, is_indel)
            if var.POS == 1110696:
                self.assertEqual(False, is_indel)
            if var.POS == 1230237:
                self.assertEqual(True, is_indel)
            elif var.POS == 1234567:
                self.assertEqual(True, is_indel)

    def test_is_transition(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            is_trans = var.is_transition
            if var.POS == 14370:
                self.assertEqual(True, is_trans)
            if var.POS == 17330:
                self.assertEqual(False, is_trans)
            if var.POS == 1110696:
                self.assertEqual(False, is_trans)
            if var.POS == 1230237:
                self.assertEqual(False, is_trans)
            elif var.POS == 1234567:
                self.assertEqual(False, is_trans)

    def test_is_deletion(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            is_del = var.is_deletion
            if var.POS == 14370:
                self.assertEqual(False, is_del)
            if var.POS == 17330:
                self.assertEqual(False, is_del)
            if var.POS == 1110696:
                self.assertEqual(False, is_del)
            if var.POS == 1230237:
                self.assertEqual(True, is_del)
            elif var.POS == 1234567:
                self.assertEqual(False, is_del)

    def test_var_type(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            type = var.var_type
            if var.POS == 14370:
                self.assertEqual('snp', type)
            if var.POS == 17330:
                self.assertEqual('snp', type)
            if var.POS == 1110696:
                self.assertEqual('snp', type)
            if var.POS == 1230237:
                self.assertEqual('indel', type)
            elif var.POS == 1234567:
                self.assertEqual('indel', type)

        reader = vcf.Reader(fh('example-4.1-sv.vcf'))
        for var in reader:
            type = var.var_type
            if var.POS == 2827693:
                self.assertEqual('sv', type)
            if var.POS == 321682:
                self.assertEqual('sv', type)
            if var.POS == 14477084:
                self.assertEqual('sv', type)
            if var.POS == 9425916:
                self.assertEqual('sv', type)
            else:
                if var.POS == 12665100:
                    self.assertEqual('sv', type)
                elif var.POS == 18665128:
                    self.assertEqual('sv', type)

    def test_var_subtype(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            subtype = var.var_subtype
            if var.POS == 14370:
                self.assertEqual('ts', subtype)
            if var.POS == 17330:
                self.assertEqual('tv', subtype)
            if var.POS == 1110696:
                self.assertEqual('unknown', subtype)
            if var.POS == 1230237:
                self.assertEqual('del', subtype)
            elif var.POS == 1234567:
                self.assertEqual('unknown', subtype)

        reader = vcf.Reader(fh('example-4.1-sv.vcf'))
        for var in reader:
            subtype = var.var_subtype
            if var.POS == 2827693:
                self.assertEqual('DEL', subtype)
            if var.POS == 321682:
                self.assertEqual('DEL', subtype)
            if var.POS == 14477084:
                self.assertEqual('DEL:ME:ALU', subtype)
            if var.POS == 9425916:
                self.assertEqual('INS:ME:L1', subtype)
            else:
                if var.POS == 12665100:
                    self.assertEqual('DUP', subtype)
                elif var.POS == 18665128:
                    self.assertEqual('DUP:TANDEM', subtype)

    def test_is_sv(self):
        reader = vcf.Reader(fh('example-4.1-sv.vcf'))
        for var in reader:
            is_sv = var.is_sv
            if var.POS == 2827693:
                self.assertEqual(True, is_sv)
            if var.POS == 321682:
                self.assertEqual(True, is_sv)
            if var.POS == 14477084:
                self.assertEqual(True, is_sv)
            if var.POS == 9425916:
                self.assertEqual(True, is_sv)
            else:
                if var.POS == 12665100:
                    self.assertEqual(True, is_sv)
                elif var.POS == 18665128:
                    self.assertEqual(True, is_sv)

        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            is_sv = var.is_sv
            if var.POS == 14370:
                self.assertEqual(False, is_sv)
            if var.POS == 17330:
                self.assertEqual(False, is_sv)
            if var.POS == 1110696:
                self.assertEqual(False, is_sv)
            if var.POS == 1230237:
                self.assertEqual(False, is_sv)
            elif var.POS == 1234567:
                self.assertEqual(False, is_sv)

    def test_is_sv_precise(self):
        reader = vcf.Reader(fh('example-4.1-sv.vcf'))
        for var in reader:
            is_precise = var.is_sv_precise
            if var.POS == 2827693:
                self.assertEqual(True, is_precise)
            if var.POS == 321682:
                self.assertEqual(False, is_precise)
            if var.POS == 14477084:
                self.assertEqual(False, is_precise)
            if var.POS == 9425916:
                self.assertEqual(False, is_precise)
            else:
                if var.POS == 12665100:
                    self.assertEqual(False, is_precise)
                elif var.POS == 18665128:
                    self.assertEqual(False, is_precise)

        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            is_precise = var.is_sv_precise
            if var.POS == 14370:
                self.assertEqual(False, is_precise)
            if var.POS == 17330:
                self.assertEqual(False, is_precise)
            if var.POS == 1110696:
                self.assertEqual(False, is_precise)
            if var.POS == 1230237:
                self.assertEqual(False, is_precise)
            elif var.POS == 1234567:
                self.assertEqual(False, is_precise)

    def test_sv_end(self):
        reader = vcf.Reader(fh('example-4.1-sv.vcf'))
        for var in reader:
            sv_end = var.sv_end
            if var.POS == 2827693:
                self.assertEqual(2827680, sv_end)
            if var.POS == 321682:
                self.assertEqual(321887, sv_end)
            if var.POS == 14477084:
                self.assertEqual(14477381, sv_end)
            if var.POS == 9425916:
                self.assertEqual(9425916, sv_end)
            else:
                if var.POS == 12665100:
                    self.assertEqual(12686200, sv_end)
                elif var.POS == 18665128:
                    self.assertEqual(18665204, sv_end)

        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            sv_end = var.sv_end
            if var.POS == 14370:
                self.assertEqual(None, sv_end)
            if var.POS == 17330:
                self.assertEqual(None, sv_end)
            if var.POS == 1110696:
                self.assertEqual(None, sv_end)
            if var.POS == 1230237:
                self.assertEqual(None, sv_end)
            elif var.POS == 1234567:
                self.assertEqual(None, sv_end)

    def test_qual(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            qual = var.QUAL
            qtype = type(qual)
            if var.POS == 14370:
                expected = 29
            if var.POS == 17330:
                expected = 3.0
            if var.POS == 1110696:
                expected = 1000.0
            if var.POS == 1230237:
                expected = 47
            elif var.POS == 1234567:
                expected = None
            self.assertEqual(expected, qual)
            self.assertEqual(type(expected), qtype)

    def test_info_multiple_values(self):
        reader = vcf.Reader(fh('example-4.1-info-multiple-values.vcf'))
        var = next(reader)
        expected = [
         19.3, 47.4, 14.0]
        actual = var.INFO['RepeatCopies']
        self.assertEqual(expected, actual)
        expected = [
         42, 14, 56]
        actual = var.INFO['RepeatSize']
        self.assertEqual(expected, actual)
        expected = [
         'TCTTATCTTCTTACTTTTCATTCCTTACTCTTACTTACTTAC', 'TTACTCTTACTTAC', 'TTACTCTTACTTACTTACTCTTACTTACTTACTCTTACTTACTTACTCTTATCTTC']
        actual = var.INFO['RepeatConsensus']
        self.assertEqual(expected, actual)

    def test_pickle(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            self.assertEqual(pickle.loads(pickle.dumps(var)), var)

    def assert_has_expected_coordinates(self, record, expected_coordinates, expected_affected_coordinates):
        self.assertEqual((
         record.start, record.end), expected_coordinates)
        self.assertEqual((
         record.affected_start, record.affected_end), expected_affected_coordinates)

    def test_coordinates_for_snp(self):
        record = model._Record('1', 10, 'id1', 'C', [
         model._Substitution('A')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 10), (9, 10))

    def test_coordinates_for_insertion(self):
        record = model._Record('1', 10, 'id2', 'C', [
         model._Substitution('CTA')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 10), (10, 10))

    def test_coordinates_for_deletion(self):
        record = model._Record('1', 10, 'id3', 'CTA', [
         model._Substitution('C')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 12), (10, 12))

    def test_coordinates_for_None_alt(self):
        record = model._Record('1', 10, 'id4', 'C', [
         None], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 10), (9, 10))

    def test_coordinates_for_multiple_snps(self):
        record = model._Record('1', 10, 'id5', 'C', [
         model._Substitution('A'),
         model._Substitution('G'),
         model._Substitution('T')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 10), (9, 10))

    def test_coordinates_for_insert_and_snp(self):
        record = model._Record('1', 10, 'id6', 'C', [
         model._Substitution('GTA'),
         model._Substitution('G')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 10), (9, 10))
        record = model._Record('1', 10, 'id7', 'C', [
         model._Substitution('G'),
         model._Substitution('GTA')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 10), (9, 10))

    def test_coordinates_for_snp_and_deletion(self):
        record = model._Record('1', 10, 'id8', 'CTA', [
         model._Substitution('C'),
         model._Substitution('CTG')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 12), (10, 12))
        record = model._Record('1', 10, 'id9', 'CTA', [
         model._Substitution('CTG'),
         model._Substitution('C')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 12), (10, 12))

    def test_coordinates_for_insertion_and_deletion(self):
        record = model._Record('1', 10, 'id10', 'CT', [
         model._Substitution('CA'),
         model._Substitution('CTT')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 11), (10, 11))
        record = model._Record('1', 10, 'id11', 'CT', [
         model._Substitution('CTT'),
         model._Substitution('CA')], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 11), (10, 11))

    def test_coordinates_for_breakend(self):
        record = model._Record('1', 10, 'id12', 'CTA', [
         model._Breakend('1', 500, False, True, 'GGTC', True)], None, None, {}, None, {}, None)
        self.assert_has_expected_coordinates(record, (9, 12), (9, 12))


class TestCall(unittest.TestCase):

    def test_dunder_eq(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        var = next(reader)
        example_call = var.samples[0]
        self.assertFalse(example_call == None)
        self.assertFalse(None == example_call)

    def test_phased(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            phases = [s.phased for s in var.samples]
            if var.POS == 14370:
                self.assertEqual([True, True, False], phases)
            if var.POS == 17330:
                self.assertEqual([True, True, False], phases)
            if var.POS == 1110696:
                self.assertEqual([True, True, False], phases)
            if var.POS == 1230237:
                self.assertEqual([True, True, False], phases)
            elif var.POS == 1234567:
                self.assertEqual([False, False, False], phases)

    def test_gt_bases(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            gt_bases = [s.gt_bases for s in var.samples]
            if var.POS == 14370:
                self.assertEqual(['G|G', 'A|G', 'A/A'], gt_bases)
            elif var.POS == 17330:
                self.assertEqual(['T|T', 'T|A', 'T/T'], gt_bases)
            else:
                if var.POS == 1110696:
                    self.assertEqual(['G|T', 'T|G', 'T/T'], gt_bases)
                else:
                    if var.POS == 1230237:
                        self.assertEqual(['T|T', 'T|T', 'T/T'], gt_bases)
                    elif var.POS == 1234567:
                        self.assertEqual([None, 'GTCT/GTACT', 'G/G'], gt_bases)

    def test_gt_types(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        for var in reader:
            for s in var:
                print(s.data)

            gt_types = [s.gt_type for s in var.samples]
            if var.POS == 14370:
                self.assertEqual([0, 1, 2], gt_types)
            elif var.POS == 17330:
                self.assertEqual([0, 1, 0], gt_types)
            else:
                if var.POS == 1110696:
                    self.assertEqual([1, 1, 2], gt_types)
                else:
                    if var.POS == 1230237:
                        self.assertEqual([0, 0, 0], gt_types)
                    elif var.POS == 1234567:
                        self.assertEqual([None, 1, 2], gt_types)


@unittest.skipUnless(pysam, 'test requires installation of PySAM.')
class TestFetch(unittest.TestCase):

    def setUp(self):
        self.reader = vcf.Reader(fh('tb.vcf.gz', 'rb'))

    def assertFetchedExpectedPositions(self, fetched_variants, expected_positions):
        fetched_positions = [var.POS for var in fetched_variants]
        self.assertEqual(fetched_positions, expected_positions)

    def testNoVariantsInRange(self):
        fetched_variants = self.reader.fetch('20', 14370, 17329)
        self.assertFetchedExpectedPositions(fetched_variants, [])

    def testNoVariantsForZeroLengthInterval(self):
        fetched_variants = self.reader.fetch('20', 14369, 14369)
        self.assertFetchedExpectedPositions(fetched_variants, [])

    def testFetchRange(self):
        fetched_variants = self.reader.fetch('20', 14369, 14370)
        self.assertFetchedExpectedPositions(fetched_variants, [14370])
        fetched_variants = self.reader.fetch('20', 14369, 17330)
        self.assertFetchedExpectedPositions(fetched_variants, [14370, 17330])
        fetched_variants = self.reader.fetch('20', 1110695, 1234567)
        self.assertFetchedExpectedPositions(fetched_variants, [1110696, 1230237, 1234567])

    def testFetchesFromStartIfStartOnlySpecified(self):
        fetched_variants = self.reader.fetch('20', 1110695)
        self.assertFetchedExpectedPositions(fetched_variants, [1110696, 1230237, 1234567])

    def testFetchesAllFromChromIfOnlyChromSpecified(self):
        fetched_variants = self.reader.fetch('20')
        self.assertFetchedExpectedPositions(fetched_variants, [
         14370, 17330, 1110696, 1230237, 1234567])


@unittest.skipUnless(pysam, 'test requires installation of PySAM.')
class TestIssue201(unittest.TestCase):

    def setUp(self):
        self.reader = vcf.Reader(fh('issue-201.vcf.gz', 'rb'), encoding='utf-8')

    def testIterate(self):
        for record in self.reader:
            pass

    def testFetch(self):
        for record in self.reader.fetch(chrom='17'):
            pass


class TestOpenMethods(unittest.TestCase):
    samples = 'NA00001 NA00002 NA00003'.split()

    def fp(self, fname):
        return os.path.join(os.path.dirname(__file__), fname)

    def testOpenFilehandle(self):
        r = vcf.Reader(fh('example-4.0.vcf'))
        self.assertEqual(self.samples, r.samples)
        self.assertEqual('example-4.0.vcf', os.path.split(r.filename)[1])

    def testOpenFilename(self):
        r = vcf.Reader(filename=self.fp('example-4.0.vcf'))
        self.assertEqual(self.samples, r.samples)

    def testOpenFilehandleGzipped(self):
        r = vcf.Reader(fh('tb.vcf.gz', 'rb'))
        self.assertEqual(self.samples, r.samples)

    def testOpenFilenameGzipped(self):
        r = vcf.Reader(filename=self.fp('tb.vcf.gz'))
        self.assertEqual(self.samples, r.samples)


class TestSampleFilter(unittest.TestCase):

    @unittest.skipUnless(IS_PYTHON2, 'test broken for Python 3')
    def testCLIListSamples(self):
        proc = subprocess.Popen('python scripts/vcf_sample_filter.py vcf/test/example-4.1.vcf', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        self.assertEqual(proc.returncode, 0)
        self.assertFalse(err)
        expected_out = ['Samples:', '0: NA00001', '1: NA00002', '2: NA00003']
        self.assertEqual(out.splitlines(), expected_out)

    @unittest.skipUnless(IS_PYTHON2, 'test broken for Python 3')
    def testCLIWithFilter(self):
        proc = subprocess.Popen('python scripts/vcf_sample_filter.py vcf/test/example-4.1.vcf -f 1,2 --quiet', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(out)
        self.assertFalse(err)
        buf = StringIO()
        buf.write(out)
        buf.seek(0)
        reader = vcf.Reader(buf)
        self.assertEqual(reader.samples, ['NA00001'])
        rec = next(reader)
        self.assertEqual(len(rec.samples), 1)

    @unittest.skipUnless(IS_NOT_PYPY, 'test broken for PyPy')
    def testSampleFilterModule(self):
        filt = vcf.SampleFilter('vcf/test/example-4.1.vcf')
        self.assertEqual(filt.samples, ['NA00001', 'NA00002', 'NA00003'])
        filtered = filt.set_filters(filters='0', invert=True)
        self.assertEqual(filtered, ['NA00001'])
        buf = StringIO()
        filt.write(buf)
        buf.seek(0)
        del filt
        self.assertTrue('sample_filter' not in dir(vcf.Reader))
        reader = vcf.Reader(buf)
        self.assertEqual(reader.samples, ['NA00001'])
        rec = next(reader)
        self.assertEqual(len(rec.samples), 1)


class TestFilter(unittest.TestCase):

    @unittest.skip('test currently broken')
    def testApplyFilter(self):
        s, out = subprocess.getstatusoutput('python scripts/vcf_filter.py --site-quality 30 test/example-4.0.vcf sq')
        self.assertEqual(s, 0)
        buf = StringIO()
        buf.write(out)
        buf.seek(0)
        print(buf.getvalue())
        reader = vcf.Reader(buf)
        assert 'sq30' in reader.filters
        print(reader.filters)
        n = 0
        for r in reader:
            if r.QUAL < 30:
                assert 'sq30' in r.FILTER
                n += 1
            elif not 'sq30' not in r.FILTER:
                raise AssertionError

        self.assertEqual(n, 2)

    @unittest.skip('test currently broken')
    def testApplyMultipleFilters(self):
        s, out = subprocess.getstatusoutput('python scripts/vcf_filter.py --site-quality 30 --genotype-quality 50 test/example-4.0.vcf sq mgq')
        self.assertEqual(s, 0)
        buf = StringIO()
        buf.write(out)
        buf.seek(0)
        reader = vcf.Reader(buf)
        print(reader.filters)
        assert 'mgq50' in reader.filters
        assert 'sq30' in reader.filters


class TestRegression(unittest.TestCase):

    def test_issue_16(self):
        reader = vcf.Reader(fh('issue-16.vcf'))
        n = next(reader)
        assert n.QUAL == None

    def test_null_mono(self):
        print(os.path.abspath(os.path.join(os.path.dirname(__file__), 'null_genotype_mono.vcf')))
        p = vcf.Reader(fh('null_genotype_mono.vcf'))
        assert p.samples
        out = StringIO()
        writer = vcf.Writer(out, p)
        for record in p:
            writer.write_record(record)

        out.seek(0)
        print(out.getvalue())
        p2 = vcf.Reader(out)
        rec = next(p2)
        assert rec.samples


class TestUtils(unittest.TestCase):

    def test_walk(self):
        reader1 = vcf.Reader(fh('example-4.0.vcf'))
        reader2 = vcf.Reader(fh('example-4.0.vcf'))
        reader3 = vcf.Reader(fh('example-4.0.vcf'))
        n = 0
        for x in utils.walk_together(reader1, reader2, reader3):
            self.assertEqual(len(x), 3)
            self.assertEqual(x[0], x[1])
            self.assertEqual(x[1], x[2])
            n += 1

        self.assertEqual(n, 5)
        expected = 'llrrttrl'
        reader1 = vcf.Reader(fh('walk_left.vcf'))
        reader2 = vcf.Reader(fh('example-4.0.vcf'))
        for ex, recs in zip(expected, utils.walk_together(reader1, reader2)):
            if ex == 'l':
                assert recs[0] is not None
                assert recs[1] is None
            if ex == 'r':
                assert recs[1] is not None
                assert recs[0] is None
                if ex == 't':
                    assert recs[0] is not None
                    if not recs[1] is not None:
                        raise AssertionError

        chr_order = list(map(str, list(range(1, 30)))) + ['X', 'Y', 'M']
        get_key = lambda r: (chr_order.index(r.CHROM.replace('chr', '')), r.POS)
        reader1 = vcf.Reader(fh('issue-140-file1.vcf'))
        reader2 = vcf.Reader(fh('issue-140-file2.vcf'))
        reader3 = vcf.Reader(fh('issue-140-file3.vcf'))
        expected = '66642577752767662466'
        for ex, recs in zip(expected, utils.walk_together(reader1, reader2, reader3, vcf_record_sort_key=get_key)):
            ex = int(ex)
            for i, flag in enumerate([4, 2, 1]):
                if ex & flag:
                    self.assertNotEqual(recs[i], None)
                else:
                    self.assertEqual(recs[i], None)

    def test_trim(self):
        tests = [
         ('TAA GAA', 'T G'),
         ('TA TA', 'T T'),
         ('AGTTTTTA AGTTTA', 'AGTT AG'),
         ('TATATATA TATATA', 'TAT T'),
         ('TATATA TATATATA', 'T TAT'),
         ('ACCCCCCC ACCCCCCCCCC ACCCCCCCCC ACCCCCCCCCCC', 'A ACCC ACC ACCCC')]
        for sequences, expected in tests:
            self.assertEqual(utils.trim_common_suffix(*sequences.split()), expected.split())


class TestGATKMeta(unittest.TestCase):

    def test_meta(self):
        reader = vcf.Reader(fh('gatk_26_meta.vcf'))
        assert 'GATKCommandLine' in reader.metadata
        self.assertEqual(reader.metadata['GATKCommandLine'][0]['CommandLineOptions'], '"analysis_type=LeftAlignAndTrimVariants"')
        self.assertEqual(reader.metadata['GATKCommandLine'][1]['CommandLineOptions'], '"analysis_type=VariantAnnotator annotation=[HomopolymerRun, VariantType, TandemRepeatAnnotator]"')


class TestUncalledGenotypes(unittest.TestCase):
    __doc__ = 'Test the handling of uncalled (., ./.) sample genotypes.'

    def test_read_uncalled(self):
        """Test that uncalled genotypes are properly read into
        gt_nums, gt_bases, ploidity, and gt_alleles properties
        of _Call objects.  For uncalled _Call objects:

        - gt_nums should be None
        - gt_bases should be None
        - ploidity should match the input ploidity
        - gt_alleles should be a list of None's with length
          matching the ploidity"""
        reader = vcf.Reader(fh('uncalled_genotypes.vcf'))
        for var in reader:
            gt_bases = [s.gt_bases for s in var.samples]
            gt_nums = [s.gt_nums for s in var.samples]
            ploidity = [s.ploidity for s in var.samples]
            gt_alleles = [s.gt_alleles for s in var.samples]
            if var.POS == 14370:
                self.assertEqual(['0|0', None, '1/1'], gt_nums)
                self.assertEqual(['G|G', None, 'A/A'], gt_bases)
                self.assertEqual([2, 2, 2], ploidity)
                self.assertEqual([['0', '0'], [None, None], ['1', '1']], gt_alleles)
            else:
                if var.POS == 17330:
                    self.assertEqual([None, '0|1', '0/0'], gt_nums)
                    self.assertEqual([None, 'T|A', 'T/T'], gt_bases)
                    self.assertEqual([3, 2, 2], ploidity)
                    self.assertEqual([[None, None, None], ['0', '1'], ['0', '0']], gt_alleles)
                elif var.POS == 1234567:
                    self.assertEqual(['0/1', '0/2', None], gt_nums)
                    self.assertEqual(['GTC/G', 'GTC/GTCT', None], gt_bases)
                    self.assertEqual([2, 2, 1], ploidity)
                    self.assertEqual([['0', '1'], ['0', '2'], [None]], gt_alleles)

        reader._reader.close()

    def test_write_uncalled(self):
        """Test that uncalled genotypes are written just as
        they were read in the input file."""
        reader = vcf.Reader(fh('uncalled_genotypes.vcf'))
        out = StringIO()
        writer = vcf.Writer(out, reader, lineterminator='\n')
        for record in reader:
            writer.write_record(record)

        reader._reader.close()
        out.seek(0)
        out_lines = out.getvalue().split('\n')
        in_file = fh('uncalled_genotypes.vcf')
        in_lines = [l.rstrip('\n') for l in in_file]
        in_file.close()
        for in_line, out_line in zip(in_lines, out_lines):
            self.assertEqual(in_line, out_line)


class TestStrelka(unittest.TestCase):

    def test_strelka(self):
        reader = vcf.Reader(fh('strelka.vcf'))
        n = next(reader)
        assert n is not None


suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestVcfSpecs))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGatkOutput))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFreebayesOutput))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSamtoolsOutput))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBcfToolsOutput))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIssue214))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test1kg))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test1kgSites))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGoNL))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStringAsFlag))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestInfoOrder))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestInfoTypeCharacter))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestParseMetaLine))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGatkOutputWriter))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBcfToolsOutputWriter))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWriterDictionaryMeta))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSamplesSpace))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMetadataWhitespace))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMixedFiltering))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRecord))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCall))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFetch))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIssue201))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOpenMethods))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSampleFilter))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFilter))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRegression))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUtils))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGATKMeta))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUncalledGenotypes))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStrelka))