# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/run.py
# Compiled at: 2019-07-30 13:57:16
# Size of source mod 2**32: 7113 bytes
__doc__ = '\nThe CLI for the EHub Model.\n\nThe options for running the model are set in the `config.yaml` file or as\ncommand-line arguments. See the `config.yaml` file for more information about\nthe `yaml` format.\n\nGiven the config.yaml file, solving the model is easy:\n\n    $ python run.py\n\nThe program will then print out the output of whatever solver is configured in\nthe config.yaml file and then the solved variables, parameters, constraints,\netc..\n\nIf you want to learn how to use `run.py` as a command-line tool, run\n\n    $ python run.py -h\n\nto learn more about the arguments.\n\nNote: You can use both the `config.yaml` and the command-line arguments\ntogether in certain situations.\n'
import argparse, os, pickle, yaml
from pyehub.energy_hub.ehub_model import EHubModel
from pyehub.logger import create_logger
from pyehub.outputter import pretty_print, output_excel, print_capacities, print_section, print_warning, stream_info
from pyehub.energy_hub.utils import constraint
DEFAULT_CONFIG_FILE = 'config.yaml'
DEFAULT_LOG_FILE = 'logs.log'

def main():
    """The main function for the CLI."""
    create_logger(DEFAULT_LOG_FILE)
    arguments = get_command_line_arguments()
    settings = parse_arguments(arguments)
    if settings['carbon']:
        model = EHubModel(excel=(settings['input_file']), max_carbon=(settings['max_carbon']), big_m=(settings['big_m']))
    else:
        model = EHubModel(excel=(settings['input_file']), big_m=(settings['big_m']))
    if settings['verbose']:
        print_section('Before_Solving', model._public_attributes())
    results = model.solve((settings['solver']), is_verbose=(settings['verbose']))
    if not settings['quiet']:
        pretty_print(results)
    output_excel((results['solution']), (settings['output_file']), time_steps=(len(model.time)),
      sheets=['other', 'capacity_storage', 'capacity_tech'])
    if settings['verbose']:
        print_capacities(results)
    print_warning(results)
    if settings['output_format']:
        stream_info(results, settings['output_file'])


def get_command_line_arguments() -> dict:
    """
    Get the arguments from the command-line and return them as a dictionary.

    Returns:
        A dictionary holding all the arguments
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', help='Suppresses all output', action='store_true',
      dest='is_quiet')
    group.add_argument('-v', '--verbose', help='Output everything', action='store_true',
      dest='is_verbose')
    parser.add_argument('--model', help='The Excel file of the model to solve', dest='input_file')
    parser.add_argument('--config', help=f"The path to the config file to use. Defaults to `{DEFAULT_CONFIG_FILE}` in the current directory. This is only used if the relevant command-line argument is not given.",
      default=DEFAULT_CONFIG_FILE,
      dest='config_file')
    parser.add_argument('--output', help='The file to output the results in', dest='output_file')
    parser.add_argument('--carbon', help='Add a maximum value to the carbon', action='store_true')
    parser.add_argument('--max_carbon', default=0, type=int, help='The maximum value that carbon can have if the --carbon switch is used.\nDefault is 0')
    parser.add_argument('--solver_options', help='The rest of the arguments are arguments to the solver', action='store_true')
    parser.add_argument('--solver', help='The solver to use', choices=[
     'glpk', 'cplex'],
      dest='solver')
    parser.add_argument('--output_format', help='Outputs the results in a different format, grouped info about streams', action='store_true')
    known, unknown = parser.parse_known_args()
    print(known, unknown)
    if not known.solver_options:
        if unknown:
            raise ValueError('Unknown arguments. Must specify `--solver_options` to allow extra arguments.')
    known = known.__dict__
    known['unknown'] = {}
    for key, value in zip(unknown[::2], unknown[1::2]):
        key = key.split('--')[(-1)]
        if key not in known['unknown']:
            known['unknown'][key] = value
        else:
            raise ValueError

    return known


def parse_arguments(arguments: dict) -> dict:
    """
    Parse the command-line arguments along with the config file.

    Args:
        arguments: The dictionary containing the command-line arguments

    Returns:
        A dictionary with the command-line arguments combined with the config
        file's settings
    """
    with open(arguments['config_file'], 'r') as (file):
        config_settings = yaml.safe_load(file)
    if not arguments['input_file']:
        input_file = config_settings['input_file']
    elif arguments['input_file']:
        input_file = arguments['input_file']
    else:
        raise ValueError('Must specify a model to solve')
    if arguments['output_file']:
        output_file = arguments['output_file']
    else:
        output_file = config_settings['output_file']
    if arguments['solver']:
        solver_name = arguments['solver']
    else:
        solver_name = config_settings['solver']['name']
    if arguments['solver_options']:
        solver_options = arguments['unknown']
    else:
        solver_options = config_settings['solver']['options']
    big_m = config_settings['BIG_M']
    return {'input_file':input_file, 
     'output_file':output_file, 
     'verbose':arguments['is_verbose'], 
     'quiet':arguments['is_quiet'], 
     'solver':{'name':solver_name, 
      'options':solver_options}, 
     'carbon':arguments['carbon'], 
     'max_carbon':arguments['max_carbon'], 
     'output_format':arguments['output_format'], 
     'big_m':big_m}


if __name__ == '__main__':
    main()