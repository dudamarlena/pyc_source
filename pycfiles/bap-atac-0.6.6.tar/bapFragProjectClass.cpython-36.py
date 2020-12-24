# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clareau/dat/Research/BuenrostroResearch/lareau_dev/bap/bap/bapFragProjectClass.py
# Compiled at: 2019-06-21 11:23:17
# Size of source mod 2**32: 11341 bytes
import click, os, os.path, sys, shutil, random, string, itertools, time, platform
from ruamel import yaml
from pkg_resources import get_distribution
from .bapHelp import *

def getBfiles(bedtools_genome, blacklist_file, reference_genome, script_dir, supported_genomes):
    """
        Function that isn't actually a bapProject specific function.
        Used to collate the built-in genomes with the possibility that the
        user specified another genome.
        """
    if bedtools_genome == '':
        if reference_genome == '':
            sys.exit('ERROR: bap needs either the bedtools genome or a correctly specified reference genome to get peaks from summit files; QUITTING')
        else:
            if any(reference_genome == s for s in supported_genomes):
                bedtoolsGenomeFile = script_dir + '/anno/bedtools/chrom_' + reference_genome + '.sizes'
            else:
                if os.path.isfile(bedtools_genome):
                    bedtoolsGenomeFile = bedtools_genome
                else:
                    sys.exit('Could not find the bedtools genome file: %s' % bedtools_genome)
    elif blacklist_file == '':
        if reference_genome == '':
            sys.exit('ERROR: bap needs either a blacklist bed file or a correctly specified reference genome to get peaks from summit files; QUITTING')
    else:
        if any(reference_genome == s for s in supported_genomes):
            blacklistFile = script_dir + '/anno/blacklist/' + reference_genome + '.full.blacklist.bed'
        else:
            if os.path.isfile(bedtools_genome):
                blacklistFile = bedtools_genome
            else:
                sys.exit('Could not find the blacklist file: %s' % bedtools_genome)
    return (
     bedtoolsGenomeFile, blacklistFile)


def mitoChr(reference_genome, mito_chromosome):
    if mito_chromosome != 'default':
        return mito_chromosome
    else:
        if reference_genome in ('hg19', 'mm10', 'hg38', 'mm10'):
            return 'chrM'
        else:
            if reference_genome in ('GRCh37', 'GRCh38', 'GRCm37', 'GRCm38'):
                return 'MT'
            if reference_genome == 'hg19_mm10_c':
                return 'humanM'
        return 'hg19_chrM'


class bapFragProject:

    def __init__(self, script_dir, supported_genomes, input, output, name, ncores, reference_genome, cluster, jobs, barcode_translate, nc_threshold, keep_temp_files, mapq, bedtools_genome, blacklist_file, tss_file, mito_chromosome, r_path, bedtools_path, samtools_path, bgzip_path, tabix_path, bead_tag):
        self.bap_version = get_distribution('bap').version
        self.script_dir = script_dir
        self.bamfile = input
        self.name = name
        self.output = output
        self.cluster = cluster
        self.jobs = jobs
        self.mapq = mapq
        self.ncores = ncores
        self.nc_threshold = nc_threshold
        self.bead_tag = bead_tag
        self.os = 'linux'
        if platform.platform()[0:5] == 'Darwi':
            self.os = 'mac'
        else:
            if name == 'default':
                filename, file_extension = os.path.splitext(self.bamfile)
                self.name = os.path.basename(filename)
            else:
                R = get_software_path('R', r_path)
                self.R = R
                bedtools = get_software_path('bedtools', bedtools_path)
                self.bedtools = bedtools
                samtools = get_software_path('samtools', samtools_path)
                self.samtools = samtools
                bgzip = get_software_path('bgzip', bgzip_path)
                self.bgzip = bgzip
                tabix = get_software_path('tabix', tabix_path)
                self.tabix = tabix
                self.reference_genome = reference_genome
                if any(self.reference_genome == s for s in supported_genomes):
                    click.echo(gettime() + 'Found designated reference genome: %s' % self.reference_genome)
                    self.tssFile = script_dir + '/anno/TSS/' + self.reference_genome + '.refGene.TSS.bed'
                    self.blacklistFile = script_dir + '/anno/blacklist/' + self.reference_genome + '.full.blacklist.bed'
                    self.bedtoolsGenomeFile = script_dir + '/anno/bedtools/chrom_' + self.reference_genome + '.sizes'
                else:
                    click.echo(gettime() + 'Could not identify this reference genome: %s' % self.reference_genome)
                    click.echo(gettime() + 'Attempting to infer necessary input files from user specification.')
                necessary = [
                 bedtools_genome, blacklist_file, tss_file, macs2_genome_size, bs_genome]
                if '' in necessary:
                    if reference_genome == '':
                        sys.exit('ERROR: specify valid reference genome with --reference-genome flag; QUITTING')
                    else:
                        sys.exit('ERROR: non-supported reference genome specified so these five must be validly specified: --bedtools-genome, --blacklist-file, --tss-file; QUITTING')
                if reference_genome in ('hg19-mm10', 'hg19_mm10_c'):
                    self.speciesMix = 'yes'
                else:
                    self.speciesMix = 'none'
            if os.path.isfile(barcode_translate):
                self.barcodeTranslateFile = barcode_translate
            else:
                sys.exit('Could not find the barcodes translate file: %s' % barcode_translate)
        if bedtools_genome != '':
            if os.path.isfile(bedtools_genome):
                self.bedtoolsGenomeFile = bedtools_genome
            else:
                sys.exit('Could not find the bedtools genome file: %s' % bedtools_genome)
        if blacklist_file != '':
            if os.path.isfile(blacklist_file):
                self.blacklistFile = blacklist_file
            else:
                sys.exit('Could not find the blacklist bed file: %s' % blacklist_file)
        if tss_file != '':
            if os.path.isfile(tss_file):
                self.tssFile = tss_file
            else:
                sys.exit('Could not find the transcription start sites file: %s' % tss_file)
        self.mitochr = mitoChr(reference_genome, mito_chromosome)

    def __iter__(self):
        yield (
         'bap_version', self.bap_version)
        yield ('script_dir', self.script_dir)
        yield ('output', self.output)
        yield ('bamfile', self.bamfile)
        yield ('name', self.name)
        yield ('ncores', self.ncores)
        yield (
         'cluster', self.cluster)
        yield ('jobs', self.jobs)
        yield (
         'barcodeTranslateFile', self.barcodeTranslateFile)
        yield (
         'nc_threshold', self.nc_threshold)
        yield ('mapq', self.mapq)
        yield (
         'tssFile', self.tssFile)
        yield ('blacklistFile', self.blacklistFile)
        yield ('bedtoolsGenomeFile', self.bedtoolsGenomeFile)
        yield ('mitochr', self.mitochr)
        yield (
         'R', self.R)
        yield ('samtools', self.samtools)
        yield ('bedtools', self.bedtools)
        yield ('bgzip', self.bgzip)
        yield ('tabix', self.tabix)
        yield (
         'bead_tag', self.bead_tag)


class bapBulkFragProject:

    def __init__(self, script_dir, supported_genomes, input, output, name, ncores, reference_genome, cluster, jobs, keep_temp_files, mapq, bedtools_genome, blacklist_file, tss_file, mito_chromosome, r_path, bedtools_path, samtools_path, bgzip_path, tabix_path):
        self.bap_version = get_distribution('bap').version
        self.script_dir = script_dir
        self.bamfile = input
        self.name = name
        self.output = output
        self.cluster = cluster
        self.jobs = jobs
        self.mapq = mapq
        self.ncores = ncores
        self.os = 'linux'
        if platform.platform()[0:5] == 'Darwi':
            self.os = 'mac'
        else:
            if name == 'default':
                filename, file_extension = os.path.splitext(self.bamfile)
                self.name = os.path.basename(filename)
            else:
                R = get_software_path('R', r_path)
                self.R = R
                bedtools = get_software_path('bedtools', bedtools_path)
                self.bedtools = bedtools
                samtools = get_software_path('samtools', samtools_path)
                self.samtools = samtools
                bgzip = get_software_path('bgzip', bgzip_path)
                self.bgzip = bgzip
                tabix = get_software_path('tabix', tabix_path)
                self.tabix = tabix
                self.reference_genome = reference_genome
                if any(self.reference_genome == s for s in supported_genomes):
                    click.echo(gettime() + 'Found designated reference genome: %s' % self.reference_genome)
                    self.tssFile = script_dir + '/anno/TSS/' + self.reference_genome + '.refGene.TSS.bed'
                    self.blacklistFile = script_dir + '/anno/blacklist/' + self.reference_genome + '.full.blacklist.bed'
                    self.bedtoolsGenomeFile = script_dir + '/anno/bedtools/chrom_' + self.reference_genome + '.sizes'
                else:
                    click.echo(gettime() + 'Could not identify this reference genome: %s' % self.reference_genome)
                    click.echo(gettime() + 'Attempting to infer necessary input files from user specification.')
                    necessary = [bedtools_genome, blacklist_file, tss_file, macs2_genome_size, bs_genome]
                    if '' in necessary:
                        if reference_genome == '':
                            sys.exit('ERROR: specify valid reference genome with --reference-genome flag; QUITTING')
                        else:
                            sys.exit('ERROR: non-supported reference genome specified so these five must be validly specified: --bedtools-genome, --blacklist-file, --tss-file; QUITTING')
            if reference_genome in ('hg19-mm10', 'hg19_mm10_c'):
                self.speciesMix = 'yes'
            else:
                self.speciesMix = 'none'
        if bedtools_genome != '':
            if os.path.isfile(bedtools_genome):
                self.bedtoolsGenomeFile = bedtools_genome
            else:
                sys.exit('Could not find the bedtools genome file: %s' % bedtools_genome)
        if blacklist_file != '':
            if os.path.isfile(blacklist_file):
                self.blacklistFile = blacklist_file
            else:
                sys.exit('Could not find the blacklist bed file: %s' % blacklist_file)
        if tss_file != '':
            if os.path.isfile(tss_file):
                self.tssFile = tss_file
            else:
                sys.exit('Could not find the transcription start sites file: %s' % tss_file)
        self.mitochr = mitoChr(reference_genome, mito_chromosome)

    def __iter__(self):
        yield (
         'bap_version', self.bap_version)
        yield ('script_dir', self.script_dir)
        yield ('output', self.output)
        yield ('bamfile', self.bamfile)
        yield ('name', self.name)
        yield ('ncores', self.ncores)
        yield (
         'cluster', self.cluster)
        yield ('jobs', self.jobs)
        yield ('mapq', self.mapq)
        yield (
         'tssFile', self.tssFile)
        yield ('blacklistFile', self.blacklistFile)
        yield ('bedtoolsGenomeFile', self.bedtoolsGenomeFile)
        yield ('mitochr', self.mitochr)
        yield (
         'R', self.R)
        yield ('samtools', self.samtools)
        yield ('bedtools', self.bedtools)
        yield ('bgzip', self.bgzip)
        yield ('tabix', self.tabix)