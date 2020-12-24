# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/fedor/Documents/dev/assnake-core-preprocessing/assnake_core_preprocessing/remove_human_bbmap/cmd_remove_human_bbmap.py
# Compiled at: 2020-02-20 15:42:38
# Size of source mod 2**32: 1609 bytes
import assnake.api.loaders, assnake.api.sample_set
from tabulate import tabulate
import click

@click.command('remove-human-bbmap', short_help='Count number of reads and basepairs in fastq file')
@click.option('--df', '-d', help='Name of the dataset', required=True)
@click.option('--preproc', '-p', help='Preprocessing to use')
@click.option('--samples-to-add', '-s', help='Samples from dataset to process',
  default='',
  metavar='<samples_to_add>',
  type=(click.STRING))
@click.pass_obj
def remove_human_bbmap(config, df, preproc, samples_to_add):
    samples_to_add = [] if samples_to_add == '' else [c.strip() for c in samples_to_add.split(',')]
    df = assnake.api.loaders.load_df_from_db(df)
    config['requested_dfs'] += [df['df']]
    ss = assnake.api.sample_set.SampleSet((df['fs_prefix']), (df['df']), preproc, samples_to_add=samples_to_add)
    click.echo(tabulate((ss.samples_pd[['fs_name', 'reads', 'preproc']].sort_values('reads')), headers='keys',
      tablefmt='fancy_grid'))
    res_list = []
    for s in ss.samples_pd.to_dict(orient='records'):
        preprocessing = s['preproc']
        res_list.append('{fs_prefix}/{df}/reads/{preproc}__rmhum_bbmap/{sample}_R1.fastq.gz'.format(fs_prefix=(s['fs_prefix'].rstrip('\\/')),
          df=(s['df']),
          preproc=preprocessing,
          sample=(s['fs_name'])))

    if config.get('requests', None) is None:
        config['requests'] = res_list
    else:
        config['requests'] += res_list