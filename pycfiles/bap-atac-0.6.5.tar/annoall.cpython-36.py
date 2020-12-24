# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/dat/Research/BuenrostroResearch/lareau_dev/bap/bap/annoall.py
# Compiled at: 2018-05-30 14:26:07
# Size of source mod 2**32: 1246 bytes
import click, os, os.path, sys, shutil, yaml, random, string, itertools, time, pysam
from pkg_resources import get_distribution
from subprocess import call, check_call
from .bapHelp import *
from .bapProjectClass import *
from ruamel import yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString as sqs

@click.command()
@click.version_option()
@click.argument('mode', type=(click.Choice(['bam'])))
@click.option('--input', '-i', help='Input for bap; varies by which mode is specified; see documentation')
@click.option('--output', '-o', default='bap_out', help='Output directory for analysis; see documentation.')
@click.option('--name', '-n', default='default', help='Name for all of the output files (default: uses the .bam prefix)')
def main(mode, input, output, name):
    """
        annotateAlleles: Annotate alleles with maternal/paternal haplotype 

        Caleb Lareau, clareau <at> broadinstitute <dot> org 

        
        mode = ['bam']

        """
    __version__ = get_distribution('bap').version
    script_dir = os.path.dirname(os.path.realpath(__file__))
    click.echo(gettime() + 'Starting annotateAlleles from bap pipeline v%s' % __version__)
    click.echo(gettime() + 'Complete.')