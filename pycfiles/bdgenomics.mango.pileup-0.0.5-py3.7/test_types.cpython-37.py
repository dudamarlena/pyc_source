# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/pileup/test/test_types.py
# Compiled at: 2019-01-29 15:49:04
# Size of source mod 2**32: 6457 bytes
import unittest
import bdgenomics.mango.pileup as pileup
from bdgenomics.mango.pileup.track import *

class TestTypes(unittest.TestCase):

    def test_track_serialization(self):
        pileup_track = pileup.Track(viz='pileup', label='myReads', source=(pileup.sources.GA4GHAlignmentJson(str)))
        serialized_track = track_to_json(pileup_track, any)
        assert serialized_track['viz'] == pileup_track.viz
        assert serialized_track['source'] == pileup_track.source
        assert serialized_track['sourceOptions'] == pileup_track.sourceOptions
        assert serialized_track['label'] == pileup_track.label
        deserialized_track = track_from_json(serialized_track, any)
        assert deserialized_track.viz == pileup_track.viz
        assert deserialized_track.source == pileup_track.source
        assert deserialized_track.sourceOptions == pileup_track.sourceOptions
        assert deserialized_track.label == pileup_track.label

    def test_tracks_serialization(self):
        sourceOptions = {'url': 'http://www.biodalliance.org/datasets/ensGene.bb'}
        gene_track = pileup.Track(viz='genes', label='myGenes', source=(pileup.sources.BigBedDataSource(sourceOptions)))
        pileup_track = pileup.Track(viz='pileup', label='myReads', source=(pileup.sources.GA4GHAlignmentJson(str)))
        tracks = [
         pileup_track, gene_track]
        serialized_tracks = tracks_to_json(tracks, any)
        assert len(serialized_tracks) == 2
        deserialized_tracks = tracks_from_json(serialized_tracks, any)
        assert len(deserialized_tracks) == 2
        assert deserialized_tracks[0].viz == 'pileup'
        assert deserialized_tracks[1].viz == 'genes'

    def test_track_invalid_viz_pileup(self):
        pileup.Track(viz='pileup', label='myReads', source=(pileup.sources.BamDataSource('fakeFile.bam')))
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='pileup', label='myReads', source=(pileup.sources.TwoBitDataSource('fakeFile.2bit')))
            self.assertTrue('Invalid data source twoBit for track pileup' in context.exception)

    def test_track_invalid_viz_coverage(self):
        pileup.Track(viz='coverage', label='myCoverage', source=(pileup.sources.BamDataSource('fakeFile.bam')))
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='coverage', label='myReads', source=(pileup.sources.TwoBitDataSource('fakeFile.2bit')))
            self.assertTrue('Invalid data source twoBit for track coverage' in context.exception)

    def test_track_invalid_viz_features(self):
        pileup.Track(viz='features', label='myFeatures', source=(pileup.sources.BigBedDataSource('fakeFile.bb')))
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='features', label='myFeatures', source=(pileup.sources.GA4GHVariantJson('{}')))
            self.assertTrue('Invalid data source variantJson for track features' in context.exception)

    def test_track_invalid_viz_genome(self):
        pileup.Track(viz='genome', label='myReference', source=(pileup.sources.TwoBitDataSource('fakeFile.2bit')))
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='genome', label='myReference', source=(pileup.sources.GA4GHFeatureJson('{}')))
            self.assertTrue('Invalid data source featureJson for track genome' in context.exception)

    def test_track_invalid_viz_variants(self):
        pileup.Track(viz='variants', label='myVariants', source=(pileup.sources.GA4GHVariantSource('www.fakeEndpoint.com', 'readGroup')))
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='variants', label='myVariants', source=(pileup.sources.GA4GHAlignmentSource('www.fakeEndpoint.com', 'readGroup')))
            self.assertTrue('Invalid data source GAReadAlignment for track variants' in context.exception)

    def test_track_invalid_viz_genes(self):
        pileup.Track(viz='genes', label='myGenes', source=(pileup.sources.BigBedDataSource('fakeFile.bb')))
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='genes', label='myGenes', source=(pileup.sources.BamDataSource('fakeFile.bam')))
            self.assertTrue('Invalid data source bam for track genes' in context.exception)

    def test_track_invalid_viz_scale(self):
        pileup.Track(viz='scale', label='scale')
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='scale', label='scale', source=(pileup.sources.BamDataSource('fakeFile.bam')))
            self.assertTrue('Invalid data source bam for track scale' in context.exception)

    def test_track_invalid_viz_location(self):
        pileup.Track(viz='location', label='location')
        with self.assertRaises(RuntimeError) as (context):
            pileup.Track(viz='location', label='location', source=(pileup.sources.BamDataSource('fakeFile.bam')))
            self.assertTrue('Invalid data source bam for track location' in context.exception)


if __name__ == '__main__':
    unittest.main()