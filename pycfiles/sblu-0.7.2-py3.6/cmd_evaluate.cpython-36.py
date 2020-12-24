# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/measure/cmd_evaluate.py
# Compiled at: 2019-11-15 16:48:30
# Size of source mod 2**32: 2379 bytes
import sys, logging
from itertools import groupby
import click, pandas as pd
from path import Path
from prody import parsePDBStream
from sblu.rmsd import srmsd
logger = logging.getLogger(__name__)

@click.command('evaluate', short_help='Evaluate ClusPro docking models.')
@click.option('--only-ca', is_flag=True, help='Only C-alpha atoms')
@click.option('--only-backbone', is_flag=True, help='Only backbone atoms')
@click.option('--only-interface', is_flag=True, help='Only interface atoms')
@click.option('--interface-radius', is_flag=True)
@click.option('--rec_bound', type=click.File(mode='r'))
@click.argument('lig_bound', type=click.File(mode='r'))
@click.argument('job_dir', type=click.Path(exists=True))
def cli(lig_bound, job_dir, only_ca, only_backbone, only_interface, interface_radius, rec_bound):

    def get_coeff(model):
        return model.basename().split('.')[1]

    def get_rank(model):
        return model.basename().split('.')[2]

    def get_lig(model):
        with open(model) as (pdbfile):
            while 1:
                line = pdbfile.readline()
                if line.startswith('END') or line.startswith('TER'):
                    break

            return parsePDBStream(pdbfile)

    directory = Path(job_dir)
    lig_crys = parsePDBStream(lig_bound)
    rec = None
    if rec_bound is not None:
        rec = parsePDBStream(rec_bound)
    models = directory.files('model*.pdb')
    logger.debug('\n'.join(models))
    lig_ags = [get_lig(m) for m in models]
    print('Calculating rmsds')
    rmsds = srmsd(lig_crys, lig_ags,
      only_ca=only_ca,
      only_backbone=only_backbone,
      only_interface=only_interface,
      interface_radius=interface_radius,
      rec=rec)
    rmsds_df = pd.DataFrame([{'coeff':get_coeff(x[0]),  'rank':get_rank(x[0]),  'path':x[0],  'rmsd':x[1]} for x in zip(models, rmsds)])
    groups = rmsds_df[(rmsds_df.rmsd <= 10)].sort_values(by='rank').groupby('coeff')
    print('First model under 10A')
    print(groups[['coeff', 'rank', 'rmsd']].head(1))
    print('Lowest overall rmsd')
    print(rmsds_df[['coeff', 'rank', 'rmsd']].sort_values(by='rmsd').groupby('coeff').head(1))