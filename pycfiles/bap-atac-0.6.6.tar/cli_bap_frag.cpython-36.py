# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clareau/dat/Research/BuenrostroResearch/lareau_dev/bap/bap/cli_bap_frag.py
# Compiled at: 2019-06-12 19:54:31
# Size of source mod 2**32: 9433 bytes
import click, os, os.path, sys, shutil, yaml, random, string, itertools, time, pysam
from pkg_resources import get_distribution
from subprocess import call, check_call
from .bapHelp import *
from .bapFragProjectClass import *
from ruamel import yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString as sqs

@click.command()
@click.version_option()
@click.option('--input', '-i', help='Input for bap-frag; varies by which mode is specified; for `bam`, .bam file with an index.')
@click.option('--output', '-o', default='bap_out', help='Output directory for analysis; this is where everything is housed.')
@click.option('--name', '-n', default='default', help='Name for all of the output files (default: uses the .bam prefix)')
@click.option('--ncores', '-c', default='detect', help='Number of cores to run the main job in parallel.')
@click.option('--reference-genome', '-r', default='hg19', help='Specifcy supported reference genome. Check `bap2 support` for a list')
@click.option('--cluster', default='', help='Message to send to Snakemake to execute jobs on cluster interface; see documentation.')
@click.option('--jobs', default='0', help='Max number of jobs to be running concurrently on the cluster interface.')
@click.option('--barcode-translate', '-be', default='', help='File path of barcodes to be pulled and renamed (.barcodesTranslate file from bap)')
@click.option('--nc-threshold', '-nc', default=6, help='Number of barcodes that a paired-end read must be observed for the read to be filtered.')
@click.option('--keep-temp-files', '-z', is_flag=True, help='Keep all intermediate files.')
@click.option('--mapq', '-mq', default=30, help='Minimum mapping quality to keep read for downstream analyses')
@click.option('--bedtools-genome', '-bg', default='', help='Path to bedtools genome file; overrides default if --reference-genome flag is set and is necessary for non-supported genomes.')
@click.option('--blacklist-file', '-bl', default='', help='Path to bed file of blacklist; overrides default if --reference-genome flag is set and is necessary for non-supported genomes.')
@click.option('--tss-file', '-ts', default='', help='Path bed file of transcription start sites; overrides default if --reference-genome flag is set and is necessary for non-supported genomes.')
@click.option('--mito-chromosome', '-mc', default='default', help='Name of the mitochondrial chromosome; only necessary to specify if the reference genome is unknown but will overwrite default if necessary')
@click.option('--r-path', default='', help='Path to R; by default, assumes that R is in PATH')
@click.option('--bedtools-path', default='', help='Path to bedtools; by default, assumes that bedtools is in PATH')
@click.option('--samtools-path', default='', help='Path to samtools; by default, assumes that samtools is in PATH')
@click.option('--bgzip-path', default='', help='Path to bgzip; by default, assumes that bgzip is in PATH')
@click.option('--tabix-path', default='', help='Path to samtools; by default, assumes that tabix is in PATH')
@click.option('--bead-tag', '-bt', default='XB', help='Tag in the .bam file(s) that point to the bead barcode.')
def main(input, output, name, ncores, reference_genome, cluster, jobs, barcode_translate, nc_threshold, keep_temp_files, mapq, bedtools_genome, blacklist_file, tss_file, mito_chromosome, r_path, bedtools_path, samtools_path, bgzip_path, tabix_path, bead_tag):
    """
        bap-frag: Extract fragments from pre-defined cells 

        Caleb Lareau, clareau <at> broadinstitute <dot> org 

        
        """
    __version__ = get_distribution('bap').version
    script_dir = os.path.dirname(os.path.realpath(__file__))
    click.echo(gettime() + 'Starting bap-frag pipeline v%s' % __version__)
    rawsg = os.popen('ls ' + script_dir + '/anno/bedtools/*.sizes').read().strip().split('\n')
    supported_genomes = [x.replace(script_dir + '/anno/bedtools/chrom_', '').replace('.sizes', '') for x in rawsg]
    if ncores == 'detect':
        ncores = str(available_cpu_count())
    else:
        ncores = str(ncores)
    snakeclust = ''
    njobs = int(jobs)
    if njobs > 0:
        if cluster != '':
            snakeclust = ' --jobs ' + str(jobs) + " --cluster '" + cluster + "' "
            click.echo(gettime() + 'Recognized flags to process jobs on a cluster.')
    else:
        if reference_genome in ('hg19-mm10', 'hg19_mm10_c'):
            speciesMix = True
        else:
            speciesMix = False
    p = bapFragProject(script_dir, supported_genomes, input, output, name, ncores, reference_genome, cluster, jobs, barcode_translate, nc_threshold, keep_temp_files, mapq, bedtools_genome, blacklist_file, tss_file, mito_chromosome, r_path, bedtools_path, samtools_path, bgzip_path, tabix_path, bead_tag)
    click.echo(gettime() + 'Attempting to parse supplied .bam files for analysis.')
    if not os.path.exists(input):
        sys.exit('Cannot parse supplied .bam file in --input')
    else:
        if not os.path.exists(input + '.bai'):
            sys.exit('Index supplied .bam before proceeding')
        idxstats = pysam.idxstats(input)
        chrs_bam = [x.split('\t')[0] for x in idxstats.split('\n')]
        chrs_ref = []
        with open(p.bedtoolsGenomeFile) as (f):
            for line in f:
                chrs_ref.append(line.split('\t')[0])

        chrs_both = intersection(chrs_bam, chrs_ref)
        if len(chrs_both) > 0:
            click.echo(gettime() + 'Found ' + str(len(chrs_both)) + ' chromosomes for analysis (including mitochondria).')
        else:
            sys.exit('Found no overlapping chromosomes between bam and reference. Check reference genome specification with the --reference-genome flag.')
    of = output
    logs = of + '/logs'
    logs_bedpe = logs + '/frag'
    fin = of + '/final'
    temp = of + '/temp'
    temp_filt_split = temp + '/filt_split'
    temp_frag_overlap = temp + '/frag_overlap'
    knee = of + '/knee'
    temp_drop_barcode = temp + '/drop_barcode'
    folders = [
     of, logs, logs_bedpe, fin, temp,
     temp_filt_split, temp_frag_overlap, temp_drop_barcode, knee,
     of + '/.internal/parseltongue', of + '/.internal/samples']
    mkfolderout = [make_folder(x) for x in folders]
    if not os.path.exists(of + '/.internal/README'):
        with open(of + '/.internal/README', 'w') as (outfile):
            outfile.write("This folder creates important (small) intermediate; don't modify it.\n\n")
    if not os.path.exists(of + '/.internal/parseltongue/README'):
        with open(of + '/.internal/parseltongue/README', 'w') as (outfile):
            outfile.write("This folder creates intermediate output to be interpreted by Snakemake; don't modify it.\n\n")
    if not os.path.exists(of + '/.internal/samples/README'):
        with open(of + '/.internal' + '/samples' + '/README', 'w') as (outfile):
            outfile.write("This folder creates samples to be interpreted by Snakemake; don't modify it.\n\n")
    click.echo(gettime() + 'Splitting input bam files by chromosome for parallel processing.')
    click.echo(gettime() + 'User specified ' + ncores + ' cores for parallel processing.')
    line1 = 'python ' + script_dir + '/bin/python/20_names_split_filt.py --input ' + p.bamfile
    line2 = ' --name ' + p.name + ' --output ' + temp_filt_split + ' --barcode-tag '
    line3 = p.bead_tag + ' --bedtools-reference-genome ' + p.bedtoolsGenomeFile
    line4 = ' --mito-chr ' + p.mitochr + ' --ncores ' + str(ncores) + ' --mapq ' + str(mapq)
    filt_split_cmd = line1 + line2 + line3 + line4
    os.system(filt_split_cmd)
    click.echo(gettime() + 'Processing per-chromosome fragments in parallel. This is the most computationally intensive step.')
    y_s = of + '/.internal/parseltongue/bap.object.bam.yaml'
    with open(y_s, 'w') as (yaml_file):
        yaml.dump((dict(p)), yaml_file, default_flow_style=False, Dumper=(yaml.RoundTripDumper))
    os.system('cp ' + y_s + ' ' + logs + '/' + p.name + '.parameters.txt')
    snake_stats = logs + '/' + p.name + '.snakemake.stats'
    snake_log = logs + '/' + p.name + '.snakemake.log'
    snakecmd_chr = 'snakemake' + snakeclust + ' --snakefile ' + script_dir + '/bin/snake/Snakefile.bap_frags --cores ' + ncores + ' --config cfp="' + y_s + '" --stats ' + snake_stats + ' &>' + snake_log
    os.system(snakecmd_chr)
    if keep_temp_files:
        click.echo(gettime() + 'Temporary files not deleted since --keep-temp-files was specified.')
    else:
        byefolder = of
        shutil.rmtree(byefolder + '/.internal')
        shutil.rmtree(byefolder + '/temp')
        click.echo(gettime() + 'Intermediate files successfully removed.')
    click.echo(gettime() + 'Complete.')