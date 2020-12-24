# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/pdb/cmd_splitsegs.py
# Compiled at: 2019-11-15 16:48:30
# Size of source mod 2**32: 727 bytes
import os, click
from sblu.pdb import parse_pdb_stream
from . import _splitsegs

@click.command('splitsegs', short_help='Split a PDB into segments suitable for psfgen.')
@click.argument('pdb_file', type=click.File(mode='r'))
@click.option('--segid/--no-segid', default=True)
@click.option('--output-prefix', default=None,
  help='Use this prefix for the output files.')
def cli(pdb_file, segid, output_prefix):
    records = parse_pdb_stream(pdb_file)
    if output_prefix is None:
        if pdb_file.name != '<stdin>':
            output_prefix = os.path.splitext(pdb_file.name)[0]
        else:
            output_prefix = 'split_pdb'
    return _splitsegs(records, segid, output_prefix)