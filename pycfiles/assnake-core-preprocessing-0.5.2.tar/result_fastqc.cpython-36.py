# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fedorov/GitHub/assnake-core-preprocessing/assnake_core_preprocessing/fastqc/result_fastqc.py
# Compiled at: 2020-03-25 13:46:41
# Size of source mod 2**32: 1017 bytes
import click
from assnake.cli.cli_utils import sample_set_construction_options, add_options, generic_command_individual_samples, generate_result_list
from assnake.core.result import Result
import os, datetime

@click.command('fastqc', short_help='Fastqc - quality control checks on raw sequence data')
@add_options(sample_set_construction_options)
@click.pass_obj
def fastqc_start(config, **kwargs):
    wc_str = config['wc_config']['fastqc_zip_wc']
    sample_set, sample_set_name = generic_command_individual_samples(config, **kwargs)
    kwargs.update({'strand': 'R1'})
    config['requests'] += generate_result_list(sample_set, wc_str, **kwargs)
    kwargs['strand'] = 'R2'
    config['requests'] += generate_result_list(sample_set, wc_str, **kwargs)


this_dir = os.path.dirname(os.path.abspath(__file__))
result_fastqc = Result.from_location(name='fastqc', location=this_dir, input_type='illumina_strand_file', additional_inputs=None, invocation_command=fastqc_start)