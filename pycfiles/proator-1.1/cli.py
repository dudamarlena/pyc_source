# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Volumes/dat/Research/BuenrostroResearch/parkour/parkour/cli.py
# Compiled at: 2016-11-02 00:48:57
import click, os, os.path, sys, shutil, shutil, random, string, logging
from pkg_resources import get_distribution
from subprocess import call, check_call

def get_subdirectories(dir):
    return [ name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))
           ]


@click.command()
@click.argument('mode')
@click.option('-o', default='p', help='Output prefix associated with sample')
@click.option('-a', default='', help='Filename/path for read 1 for sample')
@click.option('-b', default='', help='Filename/path for read 2 for sample')
@click.option('-u', is_flag=True, help='Leave output .fastq files uncompressed?')
@click.option('-s', default='-p 0.01 --nomodel', help='String of arguments to pass to MACS2; default = "-p 0.01 --nomodel"')
@click.option('-q', is_flag=True, help='Skip QC report generation? (Requires R + dependent packages (see README))')
@click.version_option()
def main(mode, o, a, b, u, s, q):
    """
        Valid MODE options include `trim`,
        
        \x08
        `trim` mode valid options:
          -a file 1
          -b file 2
        
        
        """
    __version__ = get_distribution('parkour').version
    modes = ['trim']
    if not any(mode in s for s in modes):
        sys.exit("ERROR: Improper mode '" + mode + "' selected")
    click.echo('Running ' + mode + ' mode in parkour v%s' % __version__)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    if mode == 'trim':
        if a == '':
            sys.exit('ERROR: Supply an argument with -a to run trim mode')
        if b == '':
            sys.exit('ERROR: Supply an argument with -b to run trim mode')
        uncmprs = str(False)
        if u:
            uncmprs = str(True)
        if not os.path.isfile(a):
            sys.exit("ERROR: File '" + a + "' specified with -a does not exist!")
        if not os.path.isfile(b):
            sys.exit("ERROR: File '" + b + "' specified with -b does not exist!")
        cmd = ['python', os.path.join(script_dir, 'pyadapter_trim.py'), '-a', str(a), '-b', str(b), '-u', str(uncmprs), '-o', str(o)]
        click.echo(cmd)
        call(cmd)
    click.echo('Done')