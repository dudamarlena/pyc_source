# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/features.py
# Compiled at: 2019-08-09 11:11:08
# Size of source mod 2**32: 3041 bytes
"""
========
Features
========
.. currentmodule:: bdgenomics.mango.features
.. autosummary::
   :toctree: _generate/

   FeatureSummary
"""
import bdgenomics.mango.pileup as pileup
from bdgenomics.mango.pileup.track import *
from bdgenomics.adam.adamContext import ADAMContext
from .utils import *

class FeatureSummary(object):
    __doc__ = ' FeatureSummary class.\n    FeatureSummary provides scrollable visualization of features based on genomic regions.\n    '

    def __init__(self, ac, dataset):
        """
        Initializes a GenomicRDD viz class.

        Args:
            :param ac: bdgenomics.adam.damContext.ADAMContext
            :param dataset: bdgenomics.adam.rdd.FeatureDataset
        """
        self.ac = ac
        self.dataset = dataset

    def viewPileup(self, contig, start, end, reference='hg19', label='Features', showPlot=True):
        """
        Visualizes a portion of this FeatureDataset in a scrollable pileup widget

        Args:
            :param contig: contig of locus to view
            :param start: start position of locus to view
            :param end: end position of locus to view
            reference: genome build. Default is hg19
            label: name of feature track
            showPlot: Disables widget, used for testing. Default is true.

        Returns:
            pileup view for features
        """
        contig_trimmed, contig_full = formatContig(contig)
        filtered = self.dataset.transform(lambda r: r.filter(((r.referenceName == contig_full) | (r.referenceName == contig_trimmed)) & (r.start < end) & (r.end > start)))
        json = self.ac._jvm.org.bdgenomics.mango.converters.GA4GHutil.featureDatasetToJSON(filtered._jvmRdd)
        if showPlot:
            tracks = [Track(viz='features', label=label, source=(pileup.sources.GA4GHFeatureJson(json)))]
            locus = '%s:%i-%i' % (contig, start, end)
            return pileup.PileupViewer(locus=locus, reference=reference, tracks=tracks)