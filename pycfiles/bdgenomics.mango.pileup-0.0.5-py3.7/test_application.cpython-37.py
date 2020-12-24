# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/pileup/test/test_application.py
# Compiled at: 2019-06-27 19:59:20
# Size of source mod 2**32: 3067 bytes
import unittest
import bdgenomics.mango.pileup as pileup

class MangoVizTest(unittest.TestCase):

    def test_genotypes(self):
        track = pileup.Track(viz='genotypes', label='myGenotypes', source=(pileup.sources.VcfDataSource('{}')))
        x = pileup.PileupViewer(locus='chr22:21340030-21340150', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track

    def test_features(self):
        track = pileup.Track(viz='features', label='myFeatures', source=(pileup.sources.GA4GHFeatureJson('{}')))
        x = pileup.PileupViewer(locus='chr17:1-250', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track

    def test_variants(self):
        track = pileup.Track(viz='variants', label='myVariants', source=(pileup.sources.GA4GHVariantJson('{}')))
        x = pileup.PileupViewer(locus='chr17:1-250', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track

    def test_pileup(self):
        track = pileup.Track(viz='pileup', label='myReads', source=(pileup.sources.GA4GHAlignmentJson('{}')))
        x = pileup.PileupViewer(locus='chr17:1-250', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track

    def test_genes(self):
        track = pileup.Track(viz='genes', label='myGenes', source=(pileup.sources.BigBedDataSource('fakeGenes.bb')))
        x = pileup.PileupViewer(locus='chr17:1-250', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track

    def test_pileup(self):
        track = pileup.Track(viz='pileup', label='myReads', source=(pileup.sources.GA4GHAlignmentJson('{}')))
        x = pileup.PileupViewer(locus='chr17:1-250', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track

    def test_genes(self):
        track = pileup.Track(viz='genes', label='myGenes', source=(pileup.sources.BigBedDataSource('fakeGenes.bb')))
        x = pileup.PileupViewer(locus='chr17:1-250', reference='hg19', tracks=[track])
        assert x.reference == 'hg19'
        assert x.tracks[0] == track


if __name__ == '__main__':
    unittest.main()