# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/pdb/cmd_psfgen.py
# Compiled at: 2018-10-15 19:16:31
# Size of source mod 2**32: 718 bytes
import logging, click
logger = logging.getLogger(__name__)

@click.command('psfgen', short_help='Helpful wrapper for psfgen')
@click.argument('segments', nargs=(-1), type=click.Path(exists=True))
@click.option('--link')
@click.option('--first')
@click.option('--last')
@click.option('--smod', default='')
@click.option('--wdir')
@click.option('--psfgen', default='psfgen')
@click.option('--nmin', default='nmin')
@click.option('--prm')
@click.option('--rtf')
@click.option('--auto-disu/--no-auto-disu', default=True)
@click.option('--xplor-psf/--no-xplor-psf', default=False)
@click.option('--osuffix')
def cli(segments, psfgen, nmin):
    """Generate a PSF file from pdb files"""
    raise NotImplementedError