# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fedorov/GitHub/assnake-core-preprocessing/assnake_core_preprocessing/trimmomatic/result.py
# Compiled at: 2020-03-25 13:57:54
# Size of source mod 2**32: 1180 bytes
import click, glob, os
from assnake.cli.cli_utils import sample_set_construction_options, add_options, generic_command_individual_samples, generate_result_list
from assnake.core.result import Result
parameters = [p.split('/')[(-1)].replace('.json', '') for p in glob.glob('/data11/bio/databases/ASSNAKE/params/tmtic/*.json')]

@click.command('trimmomatic', short_help='Quality based trimming')
@click.option('--params', help=('Parameters id to use. Available parameter sets: ' + str(parameters)), required=False, default='def')
@add_options(sample_set_construction_options)
@click.pass_obj
def trimmomatic_invocation(config, params, **kwargs):
    wc_str = '{fs_prefix}/{df}/reads/{preproc}__tmtic_{params}/{sample}_R1.fastq.gz'
    kwargs.update({'params': params})
    sample_set, sample_set_name = generic_command_individual_samples(config, **kwargs)
    config['requests'] += generate_result_list(sample_set, wc_str, **kwargs)


this_dir = os.path.dirname(os.path.abspath(__file__))
result = Result.from_location(name='trimmomatic', location=this_dir, input_type='illumina_sample', additional_inputs=None, invocation_command=trimmomatic_invocation)