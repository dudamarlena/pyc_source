# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fedorov/GitHub/assnake-core-preprocessing/assnake_core_preprocessing/multiqc/cmd_multiqc.py
# Compiled at: 2020-03-25 14:18:55
# Size of source mod 2**32: 2285 bytes
import click
from assnake.utils import read_yaml, pathizer
import datetime, os
from pathlib import Path

@click.command('multiqc', short_help='Forming the multiqc report')
@click.option('--df', '-d', help='Name of the dataset', required=True)
@click.option('--preproc', '-p', help='Preprocessing to use')
@click.option('--meta-column', '-c', help='Select samples based on metadata column')
@click.option('--column-value', '-v', help='Value of metadata column by which select samples')
@click.option('--samples-to-add', '-s', help='Samples from dataset to process',
  default='',
  metavar='<samples_to_add>',
  type=(click.STRING))
@click.option('--set-name', '-n', help='Name of the set', default='', type=(click.STRING))
@click.pass_obj
def multiqc_invocation(config, df, preproc, meta_column, column_value, samples_to_add, set_name):
    multiqc_report_wc = read_yaml(Path(__file__).parent.absolute() / 'wc_config.yaml')['multiqc_report_wc']
    ss, df_loaded = format_cmdinp2obj(config, df, preproc, meta_column, column_value, samples_to_add)
    if set_name == '':
        if meta_column is None:
            if column_value is None:
                curr_date = datetime.datetime.now()
                def_name = '{df}_{preproc}_{month}{year}'.format(df=df, preproc=preproc, month=(curr_date.strftime('%b')), year=(curr_date.strftime('%y')))
                set_name = def_name
        else:
            set_name = meta_column + '__' + column_value
    else:
        prepare_fastqc_list_multiqc(sample_setObj=ss, set_name=set_name, strand='R1')
        prepare_fastqc_list_multiqc(sample_setObj=ss, set_name=set_name, strand='R2')
        res_list = [
         multiqc_report_wc.format(fs_prefix=(df_loaded['fs_prefix']), df=(df_loaded['df']), sample_set=set_name, strand='R1'),
         multiqc_report_wc.format(fs_prefix=(df_loaded['fs_prefix']), df=(df_loaded['df']), sample_set=set_name, strand='R2')]
        if config.get('requests', None) is None:
            config['requests'] = res_list
        else:
            config['requests'] += res_list