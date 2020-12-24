# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/variants.py
# Compiled at: 2019-08-09 11:11:08
# Size of source mod 2**32: 3021 bytes
"""
========
Variants
========
.. currentmodule:: bdgenomics.mango.variants
.. autosummary::
   :toctree: _generate/

   VariantSummary
"""
import bdgenomics.mango.pileup as pileup
from bdgenomics.mango.pileup.track import *
from bdgenomics.adam.adamContext import ADAMContext
from .utils import *

class VariantSummary(object):
    __doc__ = ' VariantSummary class.\n    VariantSummary provides scrollable visualization of variants based on genomic regions.\n    '

    def __init__(self, ac, dataset):
        """
        Initializes a GenomicDataset viz class.

        Args:
            :param ac: bdgenomics.adamContext.ADAMContext
            :param dataset: bdgenomics.adam.rdd.VariantDataset
        """
        self.ac = ac
        self.dataset = dataset

    def viewPileup(self, contig, start, end, reference='hg19', label='Variants', showPlot=True):
        """
        Visualizes a portion of this VariantRDD in a scrollable pileup widget

        Args:
            :param contig: contig of locus to view
            :param start: start position of locus to view
            :param end: end position of locus to view
            reference: genome build. Default is hg19
            label: name of variant track
            showPlot: Disables widget, used for testing. Default is true.

        Returns:
            pileup view for variants
        """
        contig_trimmed, contig_full = formatContig(contig)
        filtered = self.dataset.transform(lambda r: r.filter(((r.referenceName == contig_full) | (r.referenceName == contig_trimmed)) & (r.start < end) & (r.end > start)))
        json = self.ac._jvm.org.bdgenomics.mango.converters.GA4GHutil.variantDatasetToJSON(filtered._jvmRdd)
        if showPlot:
            tracks = [Track(viz='variants', label=label, source=(pileup.sources.GA4GHVariantJson(json)))]
            locus = '%s:%i-%i' % (contig, start, end)
            return pileup.PileupViewer(locus=locus, reference=reference, tracks=tracks)