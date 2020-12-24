# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/viz.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 2375 bytes
__doc__ = '\nVersion of the CLI file that includes PyCallGraph calls'
from collections import OrderedDict
from contextlib import redirect_stdout
import numpy as np, pandas as pd
from config import SETTINGS
from energy_hub import EHubModel
from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput

def print_section(section_name: str, solution_section: dict) -> None:
    """
    Print all the attributes with a heading.

    Args:
        section_name: The heading
        solution_section: The dictionary with all the attributes
    """
    half_heading = '=========='
    print(f"\n{half_heading} {section_name} {half_heading}")
    attributes = OrderedDict(sorted(solution_section.items()))
    for name, value in attributes.items():
        if isinstance(value, dict):
            value = pd.DataFrame.from_dict(value, orient='index')
            if list(value.columns) == [0]:
                value.columns = [
                 name]
        print(f"\n{name}: \n{value}")


def pretty_print(results: dict) -> None:
    """Print the results in a prettier format.

    Args:
        results: The results dictionary to print
    """
    np.set_printoptions(linewidth=1000, suppress=True)
    version = results['version']
    solver = results['solver']
    print('Version: {}'.format(version))
    print('Solver')
    print('time: {}'.format(solver['time']))
    print('termination condition: {}'.format(solver['termination_condition']))
    print('Solution')
    print_section('Objective', results['solution']['objective'])
    print_section('Sets', results['solution']['sets'])
    print_section('Parameters', results['solution']['parameters'])
    print_section('Variable Parameters', results['solution']['param_or_var'])
    print_section('Variables', results['solution']['variables'])


def main():
    config = Config(l='circo')
    graphviz = GraphvizOutput(output_file='filter_none.svg', font_size=40, output_type='svg')
    with PyCallGraph(output=graphviz, config=config):
        model = EHubModel(excel=(SETTINGS['input_file']))
        results = model.solve()
        pretty_print(results)
        with open(SETTINGS['output_file'], 'w') as (file):
            with redirect_stdout(file):
                pretty_print(results)


if __name__ == '__main__':
    main()