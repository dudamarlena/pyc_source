# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/genotypes.py
# Compiled at: 2019-08-09 11:11:08
# Size of source mod 2**32: 10882 bytes
"""
=========
Genotypes
=========
.. currentmodule:: bdgenomics.mango.genotypes
.. autosummary::
   :toctree: _generate/

   GenotypeSummary
   VariantsPerSampleDistribution
   HetHomRatioDistribution
   GenotypeCallRatesDistribution
"""
import bdgenomics.mango.pileup as pileup
from bdgenomics.mango.pileup.track import *
from pyspark.sql.functions import col, expr, when
from .utils import *
from .distribution import HistogramDistribution
import matplotlib.pyplot as plt
plt.rcdefaults()

class GenotypeSummary(object):
    __doc__ = 'GenotypeSummary class.\n    GenotypeSummary provides visualizations for genotype based summaries.\n    '

    def __init__(self, spark, ac, genotypeDataset, sample=1.0):
        """
        Initializes an GenotypeSummary class.

        Args:
            :param spark: SparkSession
            :param ac: bdgenomics.adam.damContext.ADAMContext
            :param genotypeDataset:  bdgenomics.adam.rdd.GenotypeDataset
            :param sample: fraction of reads to sample from
        """
        if sample <= 0 or sample > 1:
            raise Exception('sample {} should be > 0 and <= 1'.format(self.sample))
        self.ss = spark
        self.ac = ac
        self.sample = sample
        self.genotypeDataset = genotypeDataset
        self.variantsPerSampleDistribution = None
        self.hetHomRatioDistribution = None
        self.genotypeCallRatesDistribution = None

    def getVariantsPerSampleDistribution(self):
        """
        Computes distribution of variant counts per sample.

        Returns:
           VariantsPerSampleDistribution object
        """
        if self.variantsPerSampleDistribution == None:
            print('Computing coverage variants per sample distribution...')
            self.variantsPerSampleDistribution = VariantsPerSampleDistribution((self.ss), (self.genotypeDataset),
              sample=(self.sample))
        return self.variantsPerSampleDistribution

    def getHetHomRatioDistribution(self):
        """
        Computes a distribution of (Heterozygote/Homozygote) ratios per sample

        Returns:
           HetHomRatioDistribution object
        """
        if self.hetHomRatioDistribution == None:
            print('Computing (Heterozygote/Homozygote) ratio distribution')
            self.hetHomRatioDistribution = HetHomRatioDistribution(self.ss, self.genotypeDataset, self.sample)
        return self.hetHomRatioDistribution

    def getGenotypeCallRatesDistribution(self):
        """
        Computes a distribution of variant CallRate (called / total_variants) per sample

        Returns:
           GenotypeCallRatesDistribution object
        """
        if self.genotypeCallRatesDistribution == None:
            print('Computing per sample callrate distribution')
            self.genotypeCallRatesDistribution = GenotypeCallRatesDistribution(self.ss, self.genotypeDataset, self.sample)
        return self.genotypeCallRatesDistribution

    def viewPileup(self, contig, start, end, reference='hg19', label='Genotypes', showPlot=True):
        """
        Visualizes a portion of this GenotypeRDD in a scrollable pileup widget

        Args:
            :param contig: contig of locus to view
            :param start: start position of locus to view
            :param end: end position of locus to view
            reference: genome build. Default is hg19
            label: name of genotype track
            showPlot: Disables widget, used for testing. Default is true.

        Returns:
            pileup view for genotypes
        """
        contig_trimmed, contig_full = formatContig(contig)
        filtered = self.genotypeDataset.transform(lambda r: r.filter(((r.referenceName == contig_full) | (r.referenceName == contig_trimmed)) & (r.start < end) & (r.end > start)))
        json = self.ac._jvm.org.bdgenomics.mango.converters.GA4GHutil.genotypeDatasetToJSON(filtered._jvmRdd)
        if showPlot:
            tracks = [Track(viz='genotypes', label=label, source=(pileup.sources.GA4GHVariantJson(json)))]
            locus = '%s:%i-%i' % (contig, start, end)
            return pileup.PileupViewer(locus=locus, reference=reference, tracks=tracks)


class VariantsPerSampleDistribution(HistogramDistribution):
    __doc__ = ' VariantsPerSampleDistribution class.\n    VariantsPerSampleDistribution computes a distribution of the count of variants per sample.\n    '

    def __init__(self, ss, genotypeDataset, sample=1.0):
        """
        Initializes a VariantsPerSampleDistributionn class.
        Computes the coverage distribution of a CoverageDataset. This dataset can have data for multiple samples.

        Args:
            :param ss: global SparkSession.
            :param genotypeDataset: bdgenomics.adam.rdd.GenotypeDataset
            :param sample: Fraction to sample GenotypeDataset. Should be between 0 and 1
        """
        self.sc = ss.sparkContext
        self.sample = sample
        self.rdd = genotypeDataset.transform(lambda r: r.filter((r.alleles[0] == 'ALT') | (r.alleles[1] == 'ALT'))).toDF().rdd.map(lambda r: (
         r['sampleId'], 1))
        HistogramDistribution.__init__(self)


class HetHomRatioDistribution(object):
    __doc__ = ' HetHomRatioDistribution class.\n    HetHomRatioDistribution computes a distribution of (Heterozygote/Homozygote) ratios from a genotypeDataset.\n    '

    def __init__(self, ss, genotypeDataset, sample=1.0):
        """
        Initializes HetHomRatioDistribution class.
        Retrieves the call rate and missing rate for each sample in a genotypeDataset

        Args:
            :param ss: global SparkSession.
            :param genotypeDataset: bdgenomics.adam.rdd.GenotypeDataset
            :param sample: Fraction to sample GenotypeDataset. Should be between 0 and 1
        """
        self.sample = sample
        new_col1 = when((col('alleles')[0] == 'REF') & (col('alleles')[1] == 'ALT'), 1).otherwise(when((col('alleles')[0] == 'ALT') & (col('alleles')[1] == 'ALT'), 2))
        genocounts = genotypeDataset.toDF().sample(False, self.sample).withColumn('hethomclass', new_col1).groupBy('sampleid', 'hethomclass').count().collect()
        data_het = {}
        data_hom = {}
        for row in genocounts:
            curr = row.asDict()
            if curr['hethomclass'] == 1:
                data_het[curr['sampleid']] = curr['count']
            if curr['hethomclass'] == 2:
                data_hom[curr['sampleid']] = curr['count']

        self.hetHomRatio = []
        for sampleid in data_hom.keys():
            if sampleid in data_het.keys():
                self.hetHomRatio.append(float(data_het[sampleid]) / float(data_hom[sampleid]))

    def plot(self, testMode=False, **kwargs):
        """
        Plots final distribution values and returns the plotted distribution as a list

        Returns:
          matplotlib axis to plot and computed data
        """
        if not testMode:
            figsize = kwargs.get('figsize', (10, 5))
            fig, ax = plt.subplots(figsize=figsize)
            hist = ax.hist((self.hetHomRatio), bins=100)
            return (ax, self.hetHomRatio)
        return (None, self.hetHomRatio)


class GenotypeCallRatesDistribution(object):
    __doc__ = ' GenotypeCallRatesDistribution class.\n    GenotypeCallRatesDistribution computes a distribution of per-sample genotype call rates from a genotypeDataset.\n    '

    def __init__(self, ss, genotypeDataset, sample=1.0):
        """
        Initializes a GenotypeCallRatesDistribution class.
        Retrieves counts of called and missing genotypes from a genotypeDataset.

        Args:
            :param ss: SparkContext
            :param genotypeDataset: bdgenomics.adam.rdd.GenotypeDataset
            :param sample: Fraction to sample GenotypeDataset. Should be between 0 and 1
        """
        self.sample = sample
        new_col1 = when(col('alleles')[0] != 'NO_CALL', 1).otherwise(when(col('alleles')[0] == 'NO_CALL', 2))
        callrateData = genotypeDataset.toDF().sample(False, self.sample).withColumn('calledstatus', new_col1).groupBy('sampleid', 'calledstatus').count().collect()
        data_called = {}
        data_missing = {}
        for row in callrateData:
            curr = row.asDict()
            if curr['calledstatus'] == 1:
                data_called[curr['sampleid']] = curr['count']
            if curr['calledstatus'] == 2:
                data_missing[curr['sampleid']] = curr['count']

        self.callRates = []
        for sampleid in data_called.keys():
            count_called = float(data_called.get(sampleid, 0))
            count_missing = float(data_missing.get(sampleid, 0))
            if count_called > 0:
                callrate = count_called / (count_called + count_missing)
                self.callRates.append(callrate)

    def plot(self, testMode=False, **kwargs):
        """
        Plots final distribution values and returns the plotted distribution as a list

        Args:
         :param testMode: if true, does not generate plot. Used for testing.

        Returns:
           matplotlib axis to plot and computed data
        """
        if not testMode:
            figsize = kwargs.get('figsize', (10, 5))
            fig, ax = plt.subplots(figsize=figsize)
            hist = ax.hist((self.callRates), bins=100)
            return (ax, self.callRates)
        return (None, self.callRates)