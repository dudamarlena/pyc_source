# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/adamContext.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 11063 bytes
"""
===========
adamContext
===========
.. currentmodule:: bdgenomics.adam.adamContext
.. autosummary::
   :toctree: _generate/

   ADAMContext
"""
from bdgenomics.adam.rdd import AlignmentDataset, CoverageDataset, FeatureDataset, FragmentDataset, GenotypeDataset, SequenceDataset, SliceDataset, VariantDataset
from bdgenomics.adam.stringency import STRICT, _toJava

class ADAMContext(object):
    __doc__ = '\n    The ADAMContext provides functions on top of a SparkContext for loading\n    genomic data.\n    '

    def __init__(self, ss):
        """
        Initializes an ADAMContext using a SparkSession.

        :param ss: The currently active pyspark.context.SparkContext.
        """
        self._sc = ss.sparkContext
        self._jvm = self._sc._jvm
        c = self._jvm.org.bdgenomics.adam.rdd.ADAMContext.ADAMContextFromSession(ss._jsparkSession)
        self._ADAMContext__jac = self._jvm.org.bdgenomics.adam.api.java.JavaADAMContext(c)

    def loadAlignments(self, filePath, stringency=STRICT):
        """
        Load alignments into an AlignmentDataset.

        Loads path names ending in:
        * .bam/.cram/.sam as BAM/CRAM/SAM format,
        * .fa/.fasta as FASTA format,
        * .fq/.fastq as FASTQ format, and
        * .ifq as interleaved FASTQ format.

        If none of these match, fall back to Parquet + Avro.

        For FASTA, FASTQ, and interleaved FASTQ formats, compressed files are supported
        through compression codecs configured in Hadoop, which by default include .gz and .bz2,
        but can include more.

        :param str filePath: The path to load the file from.
        :param stringency: The validation stringency to apply. Defaults to STRICT.
        :return: Returns a genomic dataset containing reads.
        :rtype: bdgenomics.adam.rdd.AlignmentDataset
        """
        adamRdd = self._ADAMContext__jac.loadAlignments(filePath, _toJava(stringency, self._jvm))
        return AlignmentDataset(adamRdd, self._sc)

    def loadIndexedBam(self, filePath, viewRegions, stringency=STRICT):
        """
        Functions like loadAlignments, but uses BAM index files to look at fewer
        blocks, and only returns records within the specified ReferenceRegions.
        BAM index file required.

        :param str pathName: The path name to load indexed BAM formatted
        alignments from. Globs/directories are supported.
        :param list<ReferenceRegion> viewRegions: List of ReferenceRegion to
        filter on.
        :param int stringency: The validation stringency to use when validating
        the BAM/CRAM/SAM format header. Defaults to ValidationStringency.STRICT.

        :return Returns an AlignmentDataset which wraps the RDD of alignment
        records, sequence dictionary representing contigs the alignments
        may be aligned to, and the read group dictionary for the alignment
        records if one is available.
        :rtype: bdgenomics.adam.rdd.AlignmentDataset
        """
        javaRrs = [rr._toJava(self._jvm) for rr in viewRegions]
        adamRdd = self._ADAMContext__jac.loadIndexedBam(filePath, javaRrs, _toJava(stringency, self._jvm))
        return AlignmentDataset(adamRdd, self._sc)

    def loadCoverage(self, filePath, stringency=STRICT):
        """
        Load features into a FeatureDataset and convert to a CoverageDataset.
        Coverage is stored in the score field of Feature.

        Loads path names ending in:
        * .bed as BED6/12 format,
        * .gff3 as GFF3 format,
        * .gtf/.gff as GTF/GFF2 format,
        * .narrow[pP]eak as NarrowPeak format, and
        * .interval_list as IntervalList format.

        If none of these match, fall back to Parquet + Avro.

        For BED6/12, GFF3, GTF/GFF2, NarrowPeak, and IntervalList formats, compressed files
        are supported through compression codecs configured in Hadoop, which by default include
        .gz and .bz2, but can include more.

        :param str filePath: The path to load coverage data from.
        :param stringency: The validation stringency to apply. Defaults to STRICT.
        :return: Returns a genomic dataset containing coverage.
        :rtype: bdgenomics.adam.rdd.CoverageDataset
        """
        adamRdd = self._ADAMContext__jac.loadCoverage(filePath, _toJava(stringency, self._jvm))
        return CoverageDataset(adamRdd, self._sc)

    def loadFragments(self, filePath, stringency=STRICT):
        """
        Load fragments into a FragmentDataset.

        Loads path names ending in:
        * .bam/.cram/.sam as BAM/CRAM/SAM format and
        * .ifq as interleaved FASTQ format.

        If none of these match, fall back to Parquet + Avro.
        For interleaved FASTQ format, compressed files are supported through compression codecs
        configured in Hadoop, which by default include .gz and .bz2, but can include more.

        :param str filePath: The path to load the file from.
        :param stringency: The validation stringency to apply. Defaults to STRICT.
        :return: Returns a genomic dataset containing sequenced fragments.
        :rtype: bdgenomics.adam.rdd.FragmentDataset
        """
        adamRdd = self._ADAMContext__jac.loadFragments(filePath, stringency)
        return FragmentDataset(adamRdd, self._sc)

    def loadFeatures(self, filePath, stringency=STRICT):
        """
        Load features into a FeatureDataset.

        Loads path names ending in:
        * .bed as BED6/12 format,
        * .gff3 as GFF3 format,
        * .gtf/.gff as GTF/GFF2 format,
        * .narrow[pP]eak as NarrowPeak format, and
        * .interval_list as IntervalList format.

        If none of these match, fall back to Parquet + Avro.

        For BED6/12, GFF3, GTF/GFF2, NarrowPeak, and IntervalList formats, compressed files
        are supported through compression codecs configured in Hadoop, which by default include
        .gz and .bz2, but can include more.

        :param str filePath: The path to load the file from.
        :param stringency: The validation stringency to apply. Defaults to STRICT.
        :return: Returns a genomic dataset containing features.
        :rtype: bdgenomics.adam.rdd.FeatureDataset
        """
        adamRdd = self._ADAMContext__jac.loadFeatures(filePath, _toJava(stringency, self._jvm))
        return FeatureDataset(adamRdd, self._sc)

    def loadGenotypes(self, filePath, stringency=STRICT):
        """
        Load genotypes into a GenotypeDataset.

        If the path name has a .vcf/.vcf.gz/.vcf.bgz extension, load as VCF format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :param stringency: The validation stringency to apply. Defaults to STRICT.
        :return: Returns a genomic dataset containing genotypes.
        :rtype: bdgenomics.adam.rdd.GenotypeDataset
        """
        adamRdd = self._ADAMContext__jac.loadGenotypes(filePath, _toJava(stringency, self._jvm))
        return GenotypeDataset(adamRdd, self._sc)

    def loadVariants(self, filePath, stringency=STRICT):
        """
        Load variants into a VariantDataset.

        If the path name has a .vcf/.vcf.gz/.vcf.bgz extension, load as VCF format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :param stringency: The validation stringency to apply. Defaults to STRICT.
        :return: Returns a genomic dataset containing variants.
        :rtype: bdgenomics.adam.rdd.VariantDataset
        """
        adamRdd = self._ADAMContext__jac.loadVariants(filePath, _toJava(stringency, self._jvm))
        return VariantDataset(adamRdd, self._sc)

    def loadDnaSequences(self, filePath):
        """
        Load DNA sequences into a SequenceDataset.

        If the path name has a .fa/.fasta extension, load as FASTA format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :return: Returns a genomic dataset containing DNA sequences.
        :rtype: bdgenomics.adam.rdd.SequenceDataset
        """
        adamRdd = self._ADAMContext__jac.loadDnaSequences(filePath)
        return SequenceDataset(adamRdd, self._sc)

    def loadProteinSequences(self, filePath):
        """
        Load protein sequences into a SequenceDataset.

        If the path name has a .fa/.fasta extension, load as FASTA format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :return: Returns a genomic dataset containing protein sequences.
        :rtype: bdgenomics.adam.rdd.SequenceDataset
        """
        adamRdd = self._ADAMContext__jac.loadProteinSequences(filePath)
        return SequenceDataset(adamRdd, self._sc)

    def loadRnaSequences(self, filePath):
        """
        Load RNA sequences into a SequenceDataset.

        If the path name has a .fa/.fasta extension, load as FASTA format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :return: Returns a genomic dataset containing RNA sequences.
        :rtype: bdgenomics.adam.rdd.SequenceDataset
        """
        adamRdd = self._ADAMContext__jac.loadRnaSequences(filePath)
        return SequenceDataset(adamRdd, self._sc)

    def loadSlices(self, filePath, maximumLength):
        """
        Load slices into a SliceDataset.

        If the path name has a .fa/.fasta extension, load as DNA in FASTA format.
        Else, fall back to Parquet + Avro.

        :param str filePath: The path to load the file from.
        :param long maximumLength: Maximum slice length.
        :return: Returns a genomic dataset containing sequence slices.
        :rtype: bdgenomics.adam.rdd.SliceDataset
        """
        adamRdd = self._ADAMContext__jac.loadSlices(filePath, maximumLength)
        return SliceDataset(adamRdd, self._sc)