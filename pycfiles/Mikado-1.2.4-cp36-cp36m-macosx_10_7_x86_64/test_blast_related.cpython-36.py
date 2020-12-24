# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/venturil/workspace/mikado/Mikado/tests/test_blast_related.py
# Compiled at: 2018-05-23 17:14:36
# Size of source mod 2**32: 3790 bytes
import tempfile
from Mikado.parsers import blast_utils
import unittest, os, gzip, subprocess, shutil, time

class BlastBasics(unittest.TestCase):

    def test_sniff_correct(self):
        valid_xml = os.path.join(os.path.dirname(__file__), 'mikado.blast.xml')
        valid, header, exc = blast_utils.BlastOpener(valid_xml).sniff()
        self.assertTrue(valid, (valid, exc))
        self.assertIsNone(exc, exc)
        with open(valid_xml, mode='rt') as (new_handle):
            valid, header, exc = blast_utils.BlastOpener(new_handle).sniff()
            self.assertTrue(valid, (valid, exc))
            self.assertIsNone(exc, exc)

    def test_sniff_invalid(self):
        invalid_xml = tempfile.NamedTemporaryFile(delete=False)
        invalid_xml.write(b'failing\n')
        invalid_xml.close()
        with self.assertRaises(ValueError):
            valid, header, exc = blast_utils.BlastOpener(invalid_xml.name).sniff()
        os.remove(invalid_xml.name)

    def test_sniff_inexistent(self):
        inexistent_xml = tempfile.mktemp()
        with self.assertRaises(OSError):
            valid, header, exc = blast_utils.BlastOpener(inexistent_xml).sniff()

    def test_sniff_gzip(self):
        new = gzip.open(tempfile.mktemp(suffix='.xml.gz'), mode='wt')
        valid_xml = os.path.join(os.path.dirname(__file__), 'mikado.blast.xml')
        with open(valid_xml) as (vx):
            for line in vx:
                new.write(line)

        new.flush()
        valid, header, exc = blast_utils.BlastOpener(new.name).sniff()
        self.assertTrue(valid, (valid, exc))
        self.assertIsNone(exc, exc)
        with gzip.open((new.name), mode='rt') as (new_handle):
            valid, header, exc = blast_utils.BlastOpener(new_handle).sniff()
            self.assertTrue(valid, (valid, exc))
            self.assertIsNone(exc, exc)

    def test_fail_closed(self):
        valid_xml = os.path.join(os.path.dirname(__file__), 'mikado.blast.xml')
        opener = blast_utils.BlastOpener(valid_xml)
        opener.close()
        with self.assertRaises(ValueError):
            opener.sniff()

    @unittest.skip
    def test_asn(self):
        master = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        valid_asn = 'mikado.blast.asn'
        with gzip.open('{0}.gz'.format(valid_asn), 'rt') as (comp_asn):
            with open(valid_asn, 'wt') as (asn):
                for line in comp_asn:
                    asn.write(line)

        with open('uniprot_sprot_plants.fasta', 'wt') as (uni_out):
            with gzip.open('uniprot_sprot_plants.fasta.gz', 'rt') as (uni):
                for line in uni:
                    uni_out.write(line)

        subprocess.call(('makeblastdb -in uniprot_sprot_plants.fasta -dbtype=prot'.format(os.path.dirname(__file__))),
          shell=True,
          stderr=(subprocess.DEVNULL),
          stdout=(subprocess.DEVNULL))
        valid, header, exc = blast_utils.BlastOpener(valid_asn).sniff()
        self.assertTrue(valid, (valid, exc))
        self.assertIsNone(exc, exc)
        valid, header, exc = blast_utils.BlastOpener('{0}.gz'.format(valid_asn)).sniff()
        self.assertTrue(valid, (valid, exc))
        self.assertIsNone(exc, exc)
        time.sleep(1)
        for fname in os.listdir('.'):
            if 'uniprot_sprot_plants.fasta' in fname and not fname.endswith('.gz'):
                os.remove(fname)

        os.remove(valid_asn)
        os.chdir(master)


if __name__ == '__main__':
    unittest.main()