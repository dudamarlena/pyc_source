# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/measure/cmd_srmsd.py
# Compiled at: 2018-10-15 19:16:31
# Size of source mod 2**32: 1367 bytes
import click
from prody import parsePDB
from sblu.rmsd import srmsd as srmsd_func

@click.command('srmsd', short_help='Single file RMSD.')
@click.argument('pdb_crys', type=click.Path(exists=True))
@click.argument('pdb_files', type=click.Path(exists=True), nargs=(-1))
@click.option('--only-CA', is_flag=True, help='Only C-alpha atoms')
@click.option('--only-backbone', is_flag=True, help='Only backbone atoms')
@click.option('--only-interface', is_flag=True, help='Only interface atoms')
@click.option('--interface-radius', type=(click.FLOAT), default=10.0)
@click.option('--rec', type=click.Path(exists=True),
  help='PDB to use for calculating interface')
@click.option('--oneline', is_flag=True)
def cli(pdb_crys, pdb_files, only_ca, only_backbone, only_interface, interface_radius, rec, oneline):
    if only_interface:
        if rec is None:
            raise click.BadOptionUsage('--only-interface requires --rec')
    else:
        crys = parsePDB(pdb_crys)
        pdbs = (parsePDB(f) for f in pdb_files)
        rec_ag = None
        if only_interface:
            rec_ag = parsePDB(rec)
        rmsds = [str(r) for r in srmsd_func(crys, pdbs, only_ca, only_backbone, only_interface, interface_radius, rec_ag)]
        sep = '\n'
        if oneline:
            sep = ','
    print(sep.join(rmsds))