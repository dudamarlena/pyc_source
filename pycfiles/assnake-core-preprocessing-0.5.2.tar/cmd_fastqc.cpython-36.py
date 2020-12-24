# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/fedor/Documents/dev/assnake-core-preprocessing/assnake_core_preprocessing/fastqc/cmd_fastqc.py
# Compiled at: 2020-02-20 15:42:38
# Size of source mod 2**32: 1215 bytes
import assnake.api.loaders, assnake.api.sample_set
from tabulate import tabulate
import click

@click.command('fastqc', short_help='Fastqc - quality control checks on raw sequence data')
@click.option('--df', '-d', help='Name of the dataset', required=True)
@click.option('--preproc', '-p', help='Preprocessing to use')
@click.option('--samples-to-add', '-s', help='Samples from dataset to process',
  default='',
  metavar='<samples_to_add>',
  type=(click.STRING))
@click.pass_obj
def fastqc_start(config, df, preproc, samples_to_add):
    samples_to_add = [] if samples_to_add == '' else [c.strip() for c in samples_to_add.split(',')]
    df = assnake.api.loaders.load_df_from_db(df)
    ss = assnake.api.sample_set.SampleSet((df['fs_prefix']), (df['df']), preproc, samples_to_add=samples_to_add)
    click.echo(tabulate((ss.samples_pd[['fs_name', 'reads', 'preproc']].sort_values('reads')), headers='keys',
      tablefmt='fancy_grid'))
    res_list = ss.get_locs_for_result('fastqc')
    if config.get('requests', None) is None:
        config['requests'] = res_list
    else:
        config['requests'] += res_list